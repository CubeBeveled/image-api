FROM python:3.13.5-slim
COPY requirements.txt /image-api
WORKDIR /image-api
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python3", "main.py"]