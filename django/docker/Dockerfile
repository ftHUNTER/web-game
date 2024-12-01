FROM python:bullseye

COPY req.txt /


RUN pip install -r req.txt

WORKDIR /var/www/html/backend

CMD [ "python" , "manage.py", "runserver", "0.0.0.0:8000"]