FROM --platform=linux/amd64 python:3.9-slim
WORKDIR /app
COPY persona_extractor.py .
RUN pip install PyMuPDF sentence-transformers torch
ENTRYPOINT ["python", "persona_extractor.py"]
