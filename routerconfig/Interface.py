"""Modulo que gerencia as interfaces de rede dos routers."""


class Interface:

    def __init__(self, name, description, full_ip):
        """Interface - Gerencia as interfaces de rede dos routers.

        :name: Nome da interface - str.
        :description: Dado descritivo da interface - str.
        :full_ip: Endereço de IP com mascara - str.
        """
        self.name = name
        self.state = 'shutdown'
        self.description = description
        self.full_ip = full_ip
        self.ip = str()
        self.mask = str()

    
    def set_ip(self, ip, mask):
        """ Pega ip passado por instância e adiciona na variável self.ip."""
        
        self.ip = ip
        self.mask = Interface.convert_cidr(mask)
    

    def write_changes(self, router):
        """ Adiciona configuracoes da interface de rede no arquivo de script do roteador."""

        router_configfile = open(f'router-config/cisco/{router.nome}.ios', 'a+')

        interface = f'interface {self.name}\n'
        ip = f'ip address {self.ip} {self.mask}\n'
        state = f'{self.state} \n'
        description = f'description {self.description} \n'

        router_configfile.write(interface)
        router_configfile.write(ip)
        router_configfile.write(state)
        router_configfile.write(description)
        router_configfile.write('exit\n')

        router_configfile.close()
    

    def shutdown(self):
        """ Desativa a interface."""

        self.state = 'shutdown'


    def no_shutdown(self):
        """ Ativa a interface. """

        self.state = 'no shutdown'


    @classmethod
    def convert_cidr(cls, cidr):
        """ TEMPORARIO, converte notaçcao em cidr para endereço completo."""

        cidr = int(cidr)

        if cidr == 24:
            return '255.255.255.0'

        elif cidr == 30:
            return '255.255.255.252'