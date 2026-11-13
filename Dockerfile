FROM python:3.13.18-slim-trixie

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN groupadd --gid 10001 app && useradd --uid 10001 --gid app --home-dir /app --no-create-home --shell /usr/sbin/nologin app
COPY database.py db_depends.py repository.py config.py main.py schemas.py routers.py services.py headers.py translations.py ./
COPY models/ ./models/

USER app:app
EXPOSE 8000
ENTRYPOINT ["python", "-m", "uvicorn"]
CMD ["main:app", "--host", "0.0.0.0", "--port", "8000"]
