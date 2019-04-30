FROM python:3.7.2-slim-stretch

ENV MININET_REPO https://github.com/mininet/mininet

RUN echo "deb http://deb.debian.org/debian sid main" >> /etc/apt/sources.list \
 && apt-get update \
 && apt-get install -y git net-tools iputils-ping dnsutils openvswitch-switch sudo \
 && apt-get clean

RUN git clone ${MININET_REPO}
RUN /mininet/util/install.sh -nf

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY start.sh topology.py /

RUN service openvswitch-switch start

#ENTRYPOINT ["/start.sh"]
ENTRYPOINT ["sleep", "infinity"]
