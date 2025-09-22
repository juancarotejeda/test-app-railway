import os
from flask import Flask, render_template_string
from flask_socketio import SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"

# SocketIO sin async_mode
socketio = SocketIO(app, cors_allowed_origins="*")

# Ruta de prueba HTTP
@app.route("/")
def index():
    return render_template_string("""
    <!doctype html>
    <html>
    <head><title>SocketIO Test</title></head>
    <body>
        <h1>Flask-SocketIO en Railway 🚀</h1>
        <button onclick="sendMessage()">Enviar mensaje</button>
        <ul id="mensajes"></ul>

        <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
        <script>
            var socket = io();

            socket.on("connect", function() {
                console.log("Conectado al servidor");
            });

            socket.on("mensaje", function(data) {
                let li = document.createElement("li");
                li.textContent = data;
                document.getElementById("mensajes").appendChild(li);
            });

            function sendMessage() {
                socket.emit("mensaje", "Hola desde el cliente");
            }
        </script>
    </body>
    </html>
    """)

# Evento WebSocket
@socketio.on("mensaje")
def manejar_mensaje(msg):
    print("Mensaje recibido:", msg)
    socketio.emit("mensaje", f"Servidor recibió: {msg}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
