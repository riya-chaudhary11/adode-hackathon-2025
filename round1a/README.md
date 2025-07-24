# Round 1A – PDF Outline Extractor

## Approach
This solution uses font size, boldness, position, and keyword cues to score and identify headings in PDF files.

## Run Instructions
```bash
docker build --platform linux/amd64 -t round1a_solution .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1a_solution
```
