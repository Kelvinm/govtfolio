FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
WORKDIR /workspace

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt