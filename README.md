# CMPE210 Course Project

This is a very simple Elixir application that makes an HTTP request to the Ryu
controller to first determine what switches are connected.

Then I make subsequent requests to pull the description of each of those switches
so that I can list the name of the switches on minimalistic the UI.

Nothing special was done on the Ryu side. I used the existing example controllers
that are already provided.

I used Elixir and Phoenix (the web framework) because I've been wanting to learn
it, so why not?

## Environment setup

1. Install docker-ce

2. Install docker-compose
```bash
pip install docker-compose
```

## Running the code
```bash
docker-compose up --build
```
When the containers come up, you will have to go inside the Mininet container
and start it up manually. This is done because we need the CLI to run commands
on each host created from Mininet. X11 forwarding does not work well inside a
VM running a container.
```bash
docker ps  # Look for the container id mininet
docker exec -it <mininet container id> bash
./start.sh
```

## Experimenting in the Mininet CLI

Make one of your hosts listen to iperf
```bash
h12 iperf -s -i 1 -u &
```
Make another host send the abost host UDP packets
```bash
perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50perf -c 10.0.0.12 -u -b 1000k -t 50
```

## Showing OpenFlow rules and meters

For convenience, open another terminal session and go inside the container.
```bash
docker exec -it <mininet container id> bash
# The topology has switches s1 and s2. Use them interchangably.
ovs-ofctl meter-stats s1 -O OpenFlow13
ovs-ofctl dump-meters s1 -O OpenFlow13
ovs-ofctl dump-flows s1 -O OpenFlow13
ovs-ofctl meter-features s1 -O OpenFlow13
```

## Inspecting the UI

When all the services are running, open a browser tab to: `<IP>:4000`
