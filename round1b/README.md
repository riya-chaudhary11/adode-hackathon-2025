# Round 1B – Persona-Based Document Intelligence

## Approach
We use a semantic model (MiniLM) to match text chunks in the documents with the given persona + job query.

## Run Instructions
```bash
docker build --platform linux/amd64 -t round1b_solution .
docker run --rm -e PERSONA="PhD Researcher" -e JOB="Literature review on GNNs" \
    -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1b_solution
```
