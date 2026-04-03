FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

# Install main packages first
RUN pip install --no-cache-dir pandas scikit-learn mlflow boto3 fastapi uvicorn

# Install DVC S3 plugin separately
RUN pip install --no-cache-dir dvc[s3]

# Copy the source code
COPY src/ /app/src/
COPY data/ /app/data/

# Expose the API port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]