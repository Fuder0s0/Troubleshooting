import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

PORT = 8080
BASE_DIR = Path(__file__).resolve().parent.parent

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        # Redireciona a raiz para /app/
        if self.path == "/" or self.path == "":
            self.send_response(302)
            self.send_header('Location', '/app/')
            self.end_headers()
            return
        return super().do_GET()

def run_server():
    os.chdir(str(BASE_DIR))
    url = f"http://localhost:{PORT}/app/"
    print("=" * 60)
    print("  SIMP-PE - Central de Troubleshooting e Soluções (MPPE)")
    print("=" * 60)
    print(f"\nIniciando servidor local em: {url}")
    print("Pressione Ctrl+C para encerrar o servidor a qualquer momento.\n")

    # Tenta abrir o navegador automaticamente
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Abra manualmente no navegador: {url}")

    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado com sucesso.")

if __name__ == "__main__":
    run_server()
