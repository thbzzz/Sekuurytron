FROM python:3.6

WORKDIR /usr/src/app

COPY sekuurytron.py .
COPY requirements.txt .
COPY token .

RUN pip install --no-cache-dir -r requirements.txt 

CMD ["python", "./sekuurytron.py"]
