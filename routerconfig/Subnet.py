
import ipaddress
from .queue import Queue


class Subnet:

    def __init__(self, name, local_mask, local_address):
        """Subnet - Gerencia o cada subnet declarada nos escopos.

        :name: Nome da subnet - str
        :local_mask: Mascara desta subnet - int.
        :local_address: Endereco da subnet - str
        """

        self.name = name
        self.local_mask = local_mask
        self.local_address = local_address
        
        self.subnet_queue = Queue()
        
        self.network_obj = ipaddress.IPv4Network((f'{self.local_address}/{self.local_mask}'))


    def ip_calculator(self):
        """ Calcula todos os endereços possiveis no CIDR e adiciona na fila de redes válidas disponiveis."""
                
        host_itter = self.network_obj.hosts()

        for host in host_itter:
            self.subnet_queue.push(host)

    def get_ip(self):
        """Retorna primeiro endereço valido da fila."""
        
        return self.subnet_queue.pop()

    def get_debug(self):
        """ Retorna string com o resultado da criacao das subnets."""

        return f'SUBNET: Criada a subnet {self.name} com endereço de rede {self.local_address}/{self.local_mask}.'