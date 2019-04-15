FROM elixir:1.8.1

RUN curl -sL https://deb.nodesource.com/setup_11.x | bash
RUN apt-get update \
 && apt-get install -y apt-utils nodejs build-essential inotify-tools

RUN mix local.hex --force \
 && mix local.rebar --force

COPY mix.exs /opt/mindcrunch/
WORKDIR /opt/mindcrunch/

RUN mix deps.get \
 && mix deps.compile

COPY assets /opt/mindcrunch/assets
RUN cd assets \
 && npm install

COPY config /opt/mindcrunch/config
COPY lib /opt/mindcrunch/lib
COPY priv /opt/mindcrunch/priv

ENTRYPOINT ["mix", "phx.server"]
