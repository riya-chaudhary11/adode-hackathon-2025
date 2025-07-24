FROM --platform=linux/amd64 python:3.9-slim
WORKDIR /app
COPY extract_outline.py .
RUN pip install PyMuPDF
ENTRYPOINT ["python", "extract_outline.py"]
