FROM python:3

WORKDIR /usr/src/app
COPY m32_chat_server.py ./

EXPOSE 7373/udp

CMD [ "python3", "./m32_chat_server.py"]