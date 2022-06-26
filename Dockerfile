FROM python:3.8

ADD main.py .

RUN pip3 install openai

CMD ["python3", "./main.py"]