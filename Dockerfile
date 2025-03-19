FROM python:alpine

WORKDIR /src

COPY ./src .

RUN  pip install --no-cache-dir -r requirements.txt

CMD ["python3", "run.py"]
