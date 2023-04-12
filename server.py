from http.server import BaseHTTPRequestHandler, HTTPServer
from time import sleep
import sys
import subprocess
import os

hostName = "192.168.1.10"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        current_time = os.popen('date').read()
        uptimes = subprocess.check_output("cat /proc/uptime", shell=True).decode('utf8').split()
        uptime = uptimes[0]

        cpu = GetCpuLoad()
        cpu_usage = cpu.getcpuload()

        processor_model = subprocess.check_output("cat /proc/cpuinfo | grep 'model name'",shell=True).decode('utf8')
        processor_speed = subprocess.check_output("cat /proc/cpuinfo | grep 'cpu MHz'", shell=True).decode('utf8')
        processor_number = subprocess.check_output("cat /proc/cpuinfo | grep 'cpu cores'", shell=True).decode('utf8')

        system_version = subprocess.check_output("cat /proc/version",shell=True).decode('utf8')

        memory_total = subprocess.check_output("cat /proc/meminfo | grep MemTotal",shell=True).decode('utf8')[10:-3]
        memory_free = subprocess.check_output("cat /proc/meminfo | grep MemFree",shell=True).decode('utf8')[9:-3]
        memory_used = str(int(memory_total) - int(memory_free))

        self.wfile.write(bytes("<html><head><title>T1 LAB SISOP</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<h1>Trabalho 1 da disciplina de Laboratorio de Sistemas Operacionais</h1>", "utf-8"))
        self.wfile.write(bytes("<h1>Gabriela Zorzo e Lucas Andreotti</h1>", "utf-8"))
        self.wfile.write(bytes("<p>Dados do servidor.</p>", "utf-8"))
        self.wfile.write(bytes("<p>Hora e hora do sistema: %s.</p>" % current_time, "utf-8"))
        self.wfile.write(bytes("<p>Uptime: %s segundos.</p>" % uptime, "utf-8"))
        self.wfile.write(bytes("<p>Modelo do processador: %s.</p>" % processor_model, "utf-8"))
        self.wfile.write(bytes("<p>Velocidade atual do processador: %s MHz.</p>" % processor_speed, "utf-8"))
        self.wfile.write(bytes("<p>Numero de processadores: %s.</p>" % processor_number, "utf-8"))
        self.wfile.write(bytes("<p>Capacidade ocupada do processador: %s%%.</p>" % cpu_usage, "utf-8"))
        self.wfile.write(bytes("<p>Memoria total: %s MB.</p>" % memory_total, "utf-8"))
        self.wfile.write(bytes("<p>Memoria livre: %s MB.</p>" % memory_free, "utf-8"))
        self.wfile.write(bytes("<p>Memoria usada: %s MB.</p>" % memory_used, "utf-8"))
        self.wfile.write(bytes("<p>Versao do sistema: %s.</p>" % system_version, "utf-8"))
        self.wfile.write(bytes("<p>Lista de processos:</p><ul>", "utf-8"))

        processes_list = subprocess.Popen(['ps','a'], stdout=subprocess.PIPE).stdout.readlines()
        for p in processes_list:
            self.wfile.write(bytes("<li> %s </li>" % p[1:-1].decode('utf-8'), "utf-8"))
        
        self.wfile.write(bytes("</ul></body></html>", "utf-8"))

class GetCpuLoad(object):
    def __init__(self, percentage=True, sleeptime = 1):
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getcputime(self):
        cpu_infos = {}
        with open(self.cpustat,'r') as f_stat:
            lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

            for cpu_line in lines:
                if '' in cpu_line: cpu_line.remove('')
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
            return cpu_infos

    def getcpuload(self):
        start = self.getcputime()
        sleep(self.sleeptime)
        stop = self.getcputime()

        cpu_load = {}

        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']

            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']
            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            cpu_load.update({cpu: CPU_Percentage})
        return cpu_load
        
if __name__ == "__main__":              
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Servidor instalado em http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")