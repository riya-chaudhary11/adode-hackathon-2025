import os
import json
import fitz
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def extract_sections(doc_path):
    doc = fitz.open(doc_path)
    sections = []
    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                text = " ".join([span["text"] for span in line["spans"]]).strip()
                if len(text) >= 20:
                    sections.append({
                        "document": os.path.basename(doc_path),
                        "page": page_num,
                        "text": text
                    })
    return sections

def rank_sections(sections, persona, job):
    query = f"{persona} - {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)
    for section in sections:
        section_embedding = model.encode(section["text"], convert_to_tensor=True)
        score = util.pytorch_cos_sim(query_embedding, section_embedding).item()
        section["score"] = score
    return sorted(sections, key=lambda x: x["score"], reverse=True)

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    persona = os.environ.get("PERSONA")
    job = os.environ.get("JOB")

    sections = []
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            sections.extend(extract_sections(os.path.join(input_dir, file)))

    ranked = rank_sections(sections, persona, job)

    output = {
        "metadata": {
            "documents": [s["document"] for s in ranked],
            "persona": persona,
            "job": job,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": [
            {
                "document": s["document"],
                "page": s["page"],
                "section_title": s["text"][:80],
                "importance_rank": i + 1
            }
            for i, s in enumerate(ranked[:10])
        ],
        "sub_section_analysis": [
            {
                "document": s["document"],
                "page": s["page"],
                "refined_text": s["text"]
            }
            for s in ranked[:10]
        ]
    }

    with open(os.path.join(output_dir, "output.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
