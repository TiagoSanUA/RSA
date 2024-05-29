FROM code.nap.av.it.pt:5050/mobility-networks/vanetza:latest
WORKDIR /
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENV EMBEDDED_MOSQUITTO_PORT_WS=8080
ENTRYPOINT ["/entrypoint.sh"]
