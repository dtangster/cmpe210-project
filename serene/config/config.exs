# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
use Mix.Config

# Configures the endpoint
config :serene, SereneWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "RQy3OuSzrZ0bk2hv1qqJ+i6oCt7F4A4iZxnAyC5D85Eooq8DvIWfWbQMqY9+O67I",
  render_errors: [view: SereneWeb.ErrorView, accepts: ~w(html json)],
  pubsub: [name: Serene.PubSub, adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env()}.exs"
