FROM python:3.12.1

WORKDIR /usr/src/app

RUN apt update && apt install -y

COPY src .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host" , "0.0.0.0", "--port", "80"]