FROM python:3.13

WORKDIR /usr/src/booksapp/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/booksapp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



