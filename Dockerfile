FROM python:3.13.18-slim-trixie

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN groupadd --gid 10001 app && useradd --uid 10001 --gid app --home-dir /app --no-create-home --shell /usr/sbin/nologin app
COPY main.py models.py routers.py services.py ./

USER app:app
EXPOSE 8000
ENTRYPOINT ["python", "-m", "uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]
