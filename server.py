from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import psutil
import platform
import os

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        t = time.localtime()
        current_time = time.asctime(t)

        cpu_usage = psutil.cpu_percent(4)

        processor_model = platform.platform()
        processor_speed = psutil.cpu_freq().current
        processor_number = os.cpu_count()

        system_version = os.uname().version

        memory_total = psutil.virtual_memory().total / 1024
        memory_used = psutil.virtual_memory().used / 1024

        self.wfile.write(bytes("<html><head><title>T1 LAB SISOP</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1>Trabalho 1 da disciplina de Laboratório de Sistemas Operacionais</h1>", "utf-8"))
        self.wfile.write(bytes("<h1>Gabriela Zorzo e Lucas Andreotti</h1>", "utf-8"))
        self.wfile.write(bytes("<p>Dados do servidor.</p>", "utf-8"))
        self.wfile.write(bytes("<p>Hora e hora do sistema: %s.</p>" % current_time, "utf-8"))
        self.wfile.write(bytes("<p>Modelo do processador: %s.</p>" % processor_model, "utf-8"))
        self.wfile.write(bytes("<p>Velocidade atual do processador: %s MHz.</p>" % processor_speed, "utf-8"))
        self.wfile.write(bytes("<p>Número de processadores: %s.</p>" % processor_number, "utf-8"))
        self.wfile.write(bytes("<p>Capacidade ocupada do processador: %s%%.</p>" % cpu_usage, "utf-8"))
        self.wfile.write(bytes("<p>Memória total: %s MB.</p>" % memory_total, "utf-8"))
        self.wfile.write(bytes("<p>Memória usada: %s MB.</p>" % memory_used, "utf-8"))
        self.wfile.write(bytes("<p>Versão do sistema: %s.</p>" % system_version, "utf-8"))
        
        self.wfile.write(bytes("</body></html>", "utf-8"))
        
if __name__ == "__main__":              
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Servidor instalado em http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")