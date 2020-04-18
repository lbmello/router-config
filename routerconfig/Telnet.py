"""Modulo que gerencia as conexoes telnet e executa os scripts."""

import telnetlib
from time import sleep

from .Basics import Basics


class Telnet:
    
    def __init__(self, router):
        """Telnet - Gerencia as conexoes telnet e executa os scripts.

        :router: Objeto de Router - obj
        """

        _script_file = open(f'router-config/cisco/{router.nome}.ios', 'r')
        
        self.router = str(router.nome)
        self.router_script = _script_file.readlines()

        self.gns_server = Basics.get_default_server_ip()
        self.gns_port = str(router.gns_port)
        
        try:
            self.telnet = telnetlib.Telnet(host=self.gns_server, port=self.gns_port)
        
        except: 
            self.telnet = False
            ConnectionRefusedError(f'TELNET: Conexão rejeitada por {self.router}.')


    def run_script(self):        
        """Roda script linha do router, linha por linha."""

        if self.telnet:
            for line in self.router_script:
                self.telnet.write(line.encode('ascii') + "\r\n".encode('ascii'))

                # Sleep para execucao do comando           
                sleep(0.3)

            self.telnet.close()

            return f'TELNET: Configuração de {self.router} concluida com sucesso.'
        
        else:
            return f'TELNET: !! Falha na configuração de {self.router}.'

    def session_close(self):
        """Encerra a sessão."""

        if self.telnet:
            self.telnet.close()

            return f'TELNET: Sessão telnet encerrada em {self.router}.'
        
        else:
            return f'TELNET: Sessão já finalizada em {self.router}.'
