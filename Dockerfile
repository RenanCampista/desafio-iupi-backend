FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD [ "sh", "-c", "python iupi/manage.py migrate && python iupi/manage.py runserver 0.0.0.0:8000" ]