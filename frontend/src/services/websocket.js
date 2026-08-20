const websocketUrl = import.meta.env.VITE_WS_URL ?? "ws://localhost:8000/ws/dashboard";

export function connectDashboardSocket({ onMessage, onStatusChange }) {
  let socket;
  let reconnectTimer;
  let closedManually = false;

  const connect = () => {
    onStatusChange?.("connecting");
    socket = new WebSocket(websocketUrl);

    socket.onopen = () => {
      onStatusChange?.("live");
    };

    socket.onmessage = (event) => {
      onMessage?.(JSON.parse(event.data));
    };

    socket.onclose = () => {
      onStatusChange?.("reconnecting");
      if (!closedManually) {
        reconnectTimer = window.setTimeout(connect, 1500);
      }
    };

    socket.onerror = () => {
      onStatusChange?.("reconnecting");
    };
  };

  connect();

  return () => {
    closedManually = true;
    window.clearTimeout(reconnectTimer);
    socket?.close();
  };
}

