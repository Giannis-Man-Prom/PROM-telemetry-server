import { io } from "socket.io-client"

class SocketioService {
  socket:any
  constructor() {}

  setupSocketConnection() {
    this.socket = io("localhost:8081")
  }
}

export default new SocketioService();