defmodule PingPong.Elixir do
  use GenServer

  def start_link do
    GenServer.start_link(__MODULE__, [], name: :ping_pong)
  end

  def init([]) do
    port = Port.open({:spawn, 'python/python_side.py'}, [:binary])
    {:ok, port}
  end

  def handle_call(:ping, _from, port) do
    json_msg = Jason.encode!(%{action: "ping"})
    send(port, {self(), json_msg})
    {:noreply, port}
  end

  def handle_info({:pong, json_msg}, port) do
    data = Jason.decode!(json_msg)
    IO.puts("Elixir: Received pong - Data: #{inspect(data)}")
    {:noreply, port}
  end
end
