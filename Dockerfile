FROM python:3

WORKDIR /usr/src/app
COPY udp_chat_server.py ./
COPY mopp.py ./
COPY config.py ./

EXPOSE 7373/udp

CMD [ "python3", "./udp_chat_server.py"]