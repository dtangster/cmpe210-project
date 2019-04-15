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

## Inspecting the UI

When all the services are running, open a browser tab to: `<IP>:4000`
