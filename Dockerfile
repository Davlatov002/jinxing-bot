# === 1-bosqich: build va dependencies ===
FROM python:3.11 AS builder

WORKDIR /web

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# === 2-bosqich: final ===
FROM python:3.11 AS final

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /web
ENV PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv
COPY . .

# Port 8000 ochiladi (runserver yoki gunicorn uchun)
EXPOSE 8000

# CMD bu yerda fallback uchun qoladi (docker-compose override qiladi)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
