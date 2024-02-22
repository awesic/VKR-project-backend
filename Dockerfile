FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/backend

COPY ./requirements.txt /app/backend/
# Build psycopg2-binary from source -- add required required dependencies
#  apk add --virtual .build-deps --no-cache postgresql-dev build-essential python3-dev musl-dev libffi-dev libpq-dev && \
RUN apt-get update && apt-get upgrade -y && apt-get install -y netcat-openbsd \ 
        && pip install wheel setuptools pip --upgrade && \
        pip install --no-cache-dir -r requirements.txt \
        # apk --purge del .build-deps \
        && rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /app/backend/
RUN sed -i 's/\r$//g' /app/backend/entrypoint.sh && \
        chmod +x /app/backend/entrypoint.sh

COPY . /app/backend/

ENTRYPOINT ["/app/backend/entrypoint.sh"]
# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
