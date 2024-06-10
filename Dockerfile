FROM python:3.12

WORKDIR /app

ADD . .

RUN pip install -r requirements.txt
RUN apt update && apt install -y libgl1-mesa-glx

CMD ["python", "run.py"]