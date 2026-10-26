
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY a2a_server.py .
COPY remote_agent.py .

EXPOSE 8001

CMD ["python", "a2a_server.py"]
