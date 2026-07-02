FROM python:3.10-slim

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"
WORKDIR /app

COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . .

EXPOSE 7860

CMD ["streamlit", "run", "web_app.py", "--server.port=7860", "--server.address=0.0.0.0"]