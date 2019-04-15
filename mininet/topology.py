#!/usr/bin/env python

from time import sleep

import docker
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def simple_topology():
    docker_client = docker.from_env()
    ip = None

    for c in docker_client.containers.list():
        for network in c.attrs['NetworkSettings']['Networks'].values():
            if 'ryu' in network['Aliases']:
                ip = network['IPAddress']
                break
        if ip:
            break

    if not ip:
        raise Exception('Failed to get controller IP')

    net = Mininet(controller=RemoteController, autoSetMacs=True)

    info('*** Adding controller\n')
    net.addController('ryu', ip=ip, port=6653)

    info('*** Adding hosts\n')
    h11 = net.addHost('h11', ip='10.0.0.11')
    h12 = net.addHost('h12', ip='10.0.0.12')
    h21 = net.addHost('h21', ip='10.0.0.21')
    h22 = net.addHost('h22', ip='10.0.0.22')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1', switch='ovsk', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', switch='ovsk', protocols='OpenFlow13')

    info('*** Creating links\n')
    net.addLink(h11, s1)
    net.addLink(h12, s1)
    net.addLink(h21, s2)
    net.addLink(h22, s2)
    net.addLink(s1, s2)

    info('*** Starting network\n')
    net.start()

    while True:
        sleep(5)


if __name__ == '__main__':
    setLogLevel('info')
    simple_topology()
