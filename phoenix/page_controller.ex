defmodule Hw2Web.PageController do
  use Hw2Web, :controller
  Application.ensure_all_started(:inets)
  Application.ensure_all_started(:ssl)

  def index(conn, _params) do
    {:ok, {{'HTTP/1.1', 200, 'OK'}, headers, body}} = :httpc.request(:get, {'http://ryu:8080/stats/switches', []}, [], [])
    {:ok, switch_ids} = Jason.decode(body)
	switch_data = Enum.map(switch_ids, fn x -> :httpc.request(:get, {'http://ryu:8080/stats/desc/' ++ Integer.to_charlist(x), []}, [], []) end)
    switch_info = Enum.map(switch_data, fn {:ok, {{'HTTP/1.1', 200, 'OK'}, headers, body}} -> Jason.decode(body) end)
    switch_names = Enum.map(switch_info, fn {x, y} -> Enum.at(Map.values(y), 0)["dp_desc"] end)
    render(conn, "index.html", switch_names: switch_names)
  end
end
