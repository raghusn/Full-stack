FROM python:3.9.16-slim

ENV LANG C.UTF-8

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt && \ 
    pip install --no-cache-dir uvicorn

RUN mkdir -p /app/src && \ 
    chgrp -R nogroup /app && \
    chmod -R 770 /app

COPY main.py /app/src/

EXPOSE 8080

CMD ["uvicorn", "app.src.main:app", "--host", "0.0.0.0", "--port", "8080"]