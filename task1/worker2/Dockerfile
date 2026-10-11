# Base image with Python 3.14.
FROM python:3.14-slim

# Disable bytecode files and enable immediate log output.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy the application into the image.
WORKDIR /app
COPY app.py /app/app.py

# Run the worker using its default container paths.
CMD ["python", "/app/app.py"]
