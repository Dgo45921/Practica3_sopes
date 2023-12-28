FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt


# CMD ["gunicorn" , "--chdir", "/usr/src/", "--worker-tmp-dir", "/dev/shm","--worker-class=gthread" ,"--workers=4", "--bind", "0.0.0.0:8080", "app:app"]