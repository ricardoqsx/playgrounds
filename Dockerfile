FROM python:alpine

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /src

COPY ./src .

CMD ["python3", "run.py"]
