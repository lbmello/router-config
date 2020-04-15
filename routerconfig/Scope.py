"""Gerencia todas as entradas de escopos, cadastradas em networks."""

import ipaddress

from .queue import Queue
from .Network import NetworkData


class Scope:

    def __init__(self, name):
        """Scope - escopo global da rede.

        :name: Nome do escopo declarado.
        """

        self.name = name
        self.subnets = NetworkData.get_scope_subnets(self.name)

        _nw_address = NetworkData.get_one_global_adress(self.name)
        _ip, _mask = _nw_address.split('/')

        self.global_address = _ip        
        self.global_mask = _mask
    
        # Instancia de fila
        self.scope_queue = Queue()

        self.subnet_calculator()
    
    
    def subnet_calculator(self):
        """ Calcula todos os endereços possiveis no CIDR e adiciona na fila redes /24 disponiveis."""
        
        cidr = ipaddress.IPv4Network((f'{self.global_address}/{self.global_mask}'))

        subnet_itter = cidr.subnets(new_prefix=24)

        for subnet_address in subnet_itter:
            self.scope_queue.push(subnet_address.network_address)


    def get_subnet(self):
        """Retorna primeiro endereço valido da fila."""
        
        return self.scope_queue.pop()


    def return_debug(self):
        """ Retorna status de criação do objeto."""

        if self:
            return f'ADDR: Criada rede {self.name} com endereço {self.global_address}/{self.global_mask}'
        else:
            return f'ADDR: Objeto ADDR não criado!'