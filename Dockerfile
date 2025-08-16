FROM python:3.12-slim

# System deps (Firefox + geckodriver setup you already had)
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz \
    && tar -xvzf geckodriver-v0.35.0-linux64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.35.0-linux64.tar.gz

# Python deps: wappalyzer (PyPI), Flask, requests
RUN pip install --no-cache-dir wappalyzer Flask requests

# App
WORKDIR /app
COPY app.py .

EXPOSE 3000

# Run the API (replaces previous ENTRYPOINT)
CMD ["python", "app.py"]
