FROM python:3.7.2-slim-stretch

ENV MININET_REPO https://github.com/mininet/mininet

RUN apt-get update \
 && apt-get install -y git net-tools iputils-ping dnsutils openvswitch-switch sudo

RUN git clone ${MININET_REPO}
RUN /mininet/util/install.sh -nfv

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY start.sh topology.py /

RUN service openvswitch-switch start

ENTRYPOINT ["/start.sh"]
