defmodule MindcrunchWeb.PageController do
  use MindcrunchWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
