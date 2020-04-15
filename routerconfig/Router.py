"""Gerencia o roteador."""


class Router:
    
    def __init__(self, nome, gns_port, ios, scope, networks, script):
        """Router - Gerencia o roteador em si.

        :nome: Nome do Roteador - str.
        :gns_port: Porta Telnet usada para conexao - str.
        :ios: Versao do IOS usada - str.
        :scope: Objeto de Escopo de rede que o router pertence - obj
        :networks: Lista com os objetos de Network para cada NIC - list.
        """
                
        self.nome = nome
        self.gns_port = gns_port
        self.ios = ios
        self.scope = scope
        self.networks = networks
        self.script = script

    def read_script(self):
        """Retorna lista com todos os comandos do arquivo de script."""
        
        script = open(f'{self.script}','r')
        
        return script.readlines()

if __name__ == "__main__":
    pass

