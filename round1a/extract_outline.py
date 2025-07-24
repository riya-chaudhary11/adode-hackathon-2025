import os
import json
import fitz  # PyMuPDF

def score_heading_candidate(span, line_idx, page_height):
    score = 0
    text = span['text'].strip()
    if span.get('flags', 0) & 2:
        score += 1
    if span['size'] > 12:
        score += 1
    if text.istitle() or text.isupper():
        score += 1
    if line_idx < 5:
        score += 1
    if any(text.lower().startswith(k) for k in ['chapter', 'section']):
        score += 1
    return score

def extract_outline_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    outlines = []
    title = os.path.basename(pdf_path).replace('.pdf', '').title()

    for page_num, page in enumerate(doc, 1):
        blocks = page.get_text('dict')['blocks']
        for line_idx, block in enumerate(blocks):
            for line in block.get('lines', []):
                text = ' '.join([span['text'] for span in line['spans']]).strip()
                if not text:
                    continue
                for span in line['spans']:
                    score = score_heading_candidate(span, line_idx, page.rect.height)
                    if score >= 3:
                        outlines.append({
                            'level': 'H1' if score >= 5 else 'H2' if score == 4 else 'H3',
                            'text': text,
                            'page': page_num
                        })
                        break
    return { 'title': title, 'outline': outlines }

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    os.makedirs(output_dir, exist_ok=True)
    for file in os.listdir(input_dir):
        if file.endswith(".pdf"):
            path = os.path.join(input_dir, file)
            result = extract_outline_from_pdf(path)
            output_path = os.path.join(output_dir, file.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
