defmodule MindcrunchWeb.RoomChannel do
  use MindcrunchWeb, :channel

  def join("room:lobby", payload, socket) do
    if authorized?(payload) do
      send(self(), :after_join)
      {:ok, socket}
    else
      {:error, %{reason: "unauthorized"}}
    end
  end

  # Channels can be used in a request/response fashion
  # by sending replies to requests from the client
  def handle_in("ping", payload, socket) do
    {:reply, {:ok, payload}, socket}
  end

  def handle_info(:after_join, socket) do
    receive do
      {:hello, msg} -> msg
    after
      1_000 ->
        push(socket, "traffic", %{bytes_tx: 10})
        handle_info(:after_join, socket)
    end
    # This will never be hit since the above will be looping
    {:noreply, socket}
  end

  # Add authorization logic here as required.
  defp authorized?(_payload) do
    true
  end
end
