defmodule MindcrunchWeb.Traffic do
  require Logger

  @doc """
  Starts accepting connections on the given `port`.
  """
  def accept(port) do
    {:ok, socket} = :gen_tcp.listen(port, [:binary, active: false])
    Logger.info "Accepting connections on port #{port}"
    loop_acceptor(socket)
  end

  defp loop_acceptor(socket) do
    {:ok, client} = :gen_tcp.accept(socket)
    {:ok, pid} = Task.Supervisor.start_child(MindcrunchWeb.Traffic.TaskSupervisor, fn -> serve(client) end)
    :ok = :gen_tcp.controlling_process(client, pid)
    loop_acceptor(socket)
  end

  defp serve(socket) do
    data = read_line(socket)
    Logger.info "Decoding JSON"
    decoded = Jason.decode!(data)
    Logger.info "Decoding successful #{decoded}"

    Logger.info "Broadcast start"
    MindcrunchWeb.Endpoint.broadcast!("room:lobby", "packet", decoded)
    Logger.info "Broadcast success"
    serve(socket)
  end

  defp read_line(socket) do
    Logger.info "Reading from socket"
    {:ok, data} = :gen_tcp.recv(socket, 0)
    data
  end
end
