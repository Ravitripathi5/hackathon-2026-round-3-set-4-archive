FROM python:latest
RUN curl -fsSL http://example.com/install.sh | bash
COPY ship.py /app/ship.py
USER root
CMD ["python", "/app/ship.py"]
