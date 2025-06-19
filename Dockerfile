# Use official Python 3.10 image (stable & compatible with spaCy)
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Install build tools for spaCy & scispaCy native dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy your project files into the image
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose default Streamlit port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
