from http.server import HTTPServer, BaseHTTPRequestHandler

class MockAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Kernel recebe o pacote TCP (SYN/ACK)
        # 2. Python monta a resposta
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        # 3. Buffer de saída escreve no socket
        self.wfile.write(b'{"status": "online", "msg": "Kernel Ack"}')

if __name__ == "__main__":
    print("--- SERVIDOR RODANDO NA PORTA 8000 (Aguardando syscall...) ---")
    server = HTTPServer(('127.0.0.1', 8000), MockAPI)
    server.serve_forever() # Loop infinito (Blocking I/O)