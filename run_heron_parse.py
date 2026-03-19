#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

import torch
from PIL import Image
from rapidocr import RapidOCR
from transformers import AutoModelForImageTextToText, AutoProcessor
from docling.datamodel.base_models import InputFormat
from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
from docling.datamodel.layout_model_specs import DOCLING_LAYOUT_HERON
from docling.datamodel.pipeline_options import (
    DocumentPictureClassifierOptions,
    LayoutOptions,
    PictureDescriptionVlmOptions,
    PdfPipelineOptions,
    RapidOcrOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode


def main() -> None:
    pdf = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("moodys-report-20250728.pdf")
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output")
    outdir.mkdir(parents=True, exist_ok=True)

    os.environ["DOCLING_ARTIFACTS_PATH"] = os.path.expanduser("~/.cache/docling/models")
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required but not available.")

    pipeline = PdfPipelineOptions(
        artifacts_path=os.environ["DOCLING_ARTIFACTS_PATH"],
        enable_remote_services=False,
        do_table_structure=True,
        do_ocr=True,
        do_chunking=True,
    )
    pipeline.do_chart_extraction = False
    pipeline.do_picture_description = True
    pipeline.picture_description_options = PictureDescriptionVlmOptions(
        repo_id="ibm-granite/granite-vision-3.3-2b",
        prompt="Describe the image and list visible numbers/labels exactly if readable.",
        generation_config={"max_new_tokens": 600, "do_sample": False},
    )
    pipeline.generate_picture_images = True
    pipeline.generate_page_images = True
    pipeline.images_scale = 3.0
    # Use RapidOCR to avoid EasyOCR model download issues in offline/local setups.
    pipeline.ocr_options = RapidOcrOptions(backend="onnxruntime", lang=["english"])
    pipeline.layout_options = LayoutOptions(model_spec=DOCLING_LAYOUT_HERON)
    pipeline.do_picture_classification = True
    pipeline.picture_classification_options = DocumentPictureClassifierOptions.from_preset(
        "document_figure_classifier_v2"
    )

    accelerator = AcceleratorOptions(device=AcceleratorDevice.CUDA, num_threads=4)

    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline, accelerator_options=accelerator)}
    )

    print(f"Parsing: {pdf}")
    print(f"Layout model: {DOCLING_LAYOUT_HERON.repo_id}")
    print("Device: CUDA")
    result = converter.convert(str(pdf))

    stem = pdf.stem
    doc = result.document
    txt_path = outdir / f"{stem}_ocr.txt"
    md_path = outdir / f"{stem}_ocr.md"
    md_embedded_path = outdir / f"{stem}_ocr_embedded.md"
    md_referenced_path = outdir / f"{stem}_ocr_referenced.md"
    md_placeholder_path = outdir / f"{stem}_ocr_placeholder.md"
    image_assets_dir = outdir / f"{stem}_images"
    summary_path = outdir / f"{stem}_summary.json"

    picture_labels = []
    if hasattr(doc, "pictures"):
        for i, pic in enumerate(doc.pictures):
            labels = []
            anns = getattr(pic, "annotations", None) or []
            for ann in anns:
                cls = getattr(ann, "predicted_classes", None) or []
                labels.extend([getattr(c, "class_name", str(c)) for c in cls])
            dedup = list(dict.fromkeys(labels))
            picture_labels.append(
                {
                    "picture_index": i,
                    "top_label": dedup[0] if dedup else None,
                    "labels": dedup,
                }
            )

    txt_path.write_text(doc.export_to_text(), encoding="utf-8")
    # Keep placeholder markdown as an explicit extra file.
    md_placeholder_path.write_text(doc.export_to_markdown(), encoding="utf-8")
    # Embedded mode stores images inline (base64) and renders directly in Markdown viewers.
    md_embedded_path.write_text(
        doc.export_to_markdown(image_mode=ImageRefMode.EMBEDDED),
        encoding="utf-8",
    )
    # Referenced mode writes image files to disk and links to them from markdown.
    doc.save_as_markdown(
        filename=md_referenced_path,
        artifacts_dir=image_assets_dir,
        image_mode=ImageRefMode.REFERENCED,
    )
    # Add classifier + OCR details under each image in markdown.
    image_files = sorted(image_assets_dir.glob("image_*.png"))
    ocr_engine = RapidOCR()
    granite_path = Path(os.environ["DOCLING_ARTIFACTS_PATH"]) / "ibm-granite--granite-vision-3.3-2b"
    if not granite_path.exists():
        raise FileNotFoundError(f"Missing local Granite model at {granite_path}")
    granite_processor = AutoProcessor.from_pretrained(str(granite_path), local_files_only=True)
    granite_model = AutoModelForImageTextToText.from_pretrained(
        str(granite_path),
        local_files_only=True,
        dtype=torch.bfloat16,
        device_map="cuda",
    )
    per_image_notes = []
    for i, img in enumerate(image_files):
        txt = ""
        granite_desc = ""
        try:
            ocr_res, _ = ocr_engine(str(img))
            if ocr_res:
                txt = " | ".join([r[1] for r in ocr_res if len(r) > 1])[:400]
        except Exception:
            txt = ""
        try:
            pil_img = Image.open(img).convert("RGB")
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": pil_img},
                        {
                            "type": "text",
                            "text": "Describe this image and list all visible numeric values/axis labels exactly if readable.",
                        },
                    ],
                }
            ]
            prompt = granite_processor.apply_chat_template(
                messages, add_generation_prompt=True, tokenize=False
            )
            inputs = granite_processor(text=prompt, images=[pil_img], return_tensors="pt").to(
                granite_model.device
            )
            out = granite_model.generate(**inputs, max_new_tokens=600, do_sample=False)
            granite_desc = granite_processor.decode(out[0], skip_special_tokens=True).split(
                "<|assistant|>"
            )[-1].strip()[:2500]
        except Exception:
            granite_desc = ""
        top = picture_labels[i]["top_label"] if i < len(picture_labels) else None
        note = (
            f"\n\n> Image details: top_label={top}; "
            f"ocr_text={txt if txt else 'N/A'}; "
            f"granite_desc={granite_desc if granite_desc else 'N/A'}\n"
        )
        per_image_notes.append(note)

    md_lines = md_referenced_path.read_text(encoding="utf-8").splitlines()
    out_lines = []
    img_idx = 0
    for line in md_lines:
        out_lines.append(line)
        if line.startswith("![Image]("):
            out_lines.append(per_image_notes[img_idx] if img_idx < len(per_image_notes) else "\n")
            img_idx += 1
    md_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    summary = {
        "layout_model": DOCLING_LAYOUT_HERON.repo_id,
        "device": "cuda",
        "pages": len(doc.pages) if hasattr(doc, "pages") else None,
        "tables": len(doc.tables) if hasattr(doc, "tables") else None,
        "images": len(doc.pictures) if hasattr(doc, "pictures") else None,
        "picture_classifier": "DocumentFigureClassifier-v2.0",
        "picture_labels": picture_labels,
        "output_txt": str(txt_path),
        "output_md": str(md_path),
        "output_md_placeholder": str(md_placeholder_path),
        "output_md_embedded": str(md_embedded_path),
        "output_md_referenced": str(md_referenced_path),
        "image_assets_dir": str(image_assets_dir),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
