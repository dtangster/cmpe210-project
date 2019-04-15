FROM elixir:1.8.1

RUN curl -sL https://deb.nodesource.com/setup_11.x | bash
RUN apt-get update \
 && apt-get install -y apt-utils nodejs build-essential inotify-tools

RUN mix local.hex --force \
 && mix archive.install --force hex phx_new 1.4.2 \
 && mix local.rebar --force

ENV APPNAME hw2
RUN mix phx.new hw2 --no-ecto
WORKDIR /hw2
RUN mix deps.get \
 && mix deps.compile \
 && cd assets \
 && npm install

COPY page_controller.ex /hw2/lib/hw2_web/controllers/
COPY index.html.eex /hw2/lib/hw2_web/templates/page/

ENTRYPOINT ["mix", "phx.server"]
