FROM python:3.9
WORKDIR /usr/src/app
COPY archivos/. ./
RUN pip install --no-cache-dir -r requirements.txt
ENV MYSQL_PASSWORD p4ssw0rd
ENV MYSQL_USER user_code
ENV MYSQL_DATABASE stori_db
ENV MYSQL_HOST 172.17.0.1
CMD [ "python", "main.py" ]