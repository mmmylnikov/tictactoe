FROM python:3.12.2-alpine

WORKDIR /app/

COPY game.py /app/

CMD [ "python", "game.py" ]
