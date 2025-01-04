FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y \
    git \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/im8otto/dbd-unlocker.git /dbd-unlocker-8otto

WORKDIR /dbd-unlocker-8otto

RUN pip3 install -r requirements.txt

EXPOSE 8082

CMD mitmdump -s Utils/Proxy.py --allow-hosts '^.*(bhvrdbd\.com|mitm\.it).*$' --quiet --set log_level=none --listen-port 8082
