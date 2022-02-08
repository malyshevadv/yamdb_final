FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
COPY /static/redoc.yaml /static_temp
COPY /static/data/* /static_temp/data/
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]