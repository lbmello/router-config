""" Classes Model e Controller de Network."""

from .Yaml import YamlReader
from .Interface import Interface


## MODEL

class NetworkData:
    """ Classe de dados para Network. """
    
    yaml = YamlReader()

    # Metodos de leitura da sessao networks do arquivo routers.yaml
    @classmethod
    def get_global_network(cls):
        """ Retorna todos os valores de networks em routers.yaml. """

        scopes = []

        for full_scope in NetworkData.yaml.networks:
            scopes_name = list(full_scope.keys())
            scopes_name = scopes_name[0]
            
            configs = (list(full_scope.values()))

            full_address = (configs[0][0]['address'])

            address = full_address.split('/')[0]
            mask = full_address.split('/')[1]

            subnets_list = ((configs[0][1]['subnets']))

            scopes_dict = {'scope_name': f'{scopes_name}', 'address': address, 'mask':mask, 'subnets': subnets_list}
            
            scopes.append(scopes_dict)
        
        return scopes

    @classmethod
    def get_scope_subnets(cls, scope_name):
        """ Retorna somente os itens de subnet de um escopo especifico."""

        for full_scope in NetworkData.yaml.networks:
            scopes_name = list(full_scope.keys())
            scopes_name = scopes_name[0]
            
            if scopes_name == scope_name:
                configs = (list(full_scope.values()))

                subnets_list = ((configs[0][1]['subnets']))
                
                return subnets_list

    @classmethod
    def get_all_global_adress(cls):
        """ Retorna somente os itens de endereço de todos os router. """

        _global_address = []

        _globals = NetworkData.get_global_network()
        for line in _globals:
            _global_address.append(f"{line['address']}/{line['mask']}")

        return _global_address

    @classmethod
    def get_one_global_adress(cls, scope_name):
        """ Retorna somente os itens de endereço de um router. """

        _globals = NetworkData.get_global_network()
        for line in _globals:
            if line['scope_name'] == scope_name:
                _global_address = (f"{line['address']}/{line['mask']}")
                print(type(_global_address))

        return _global_address
    

    @classmethod
    def get_global_name(cls):
        """ Retorna somente os itens de nome de um router específico. """

        _global_name = []

        _globals = NetworkData.get_global_network()
        for line in _globals:
            _global_name.append(line['scope_name'])

        return _global_name

    
    # Metodos para leitura dos roteadores de routers.yaml
    @classmethod
    def get_router_config(cls, router_obj):
        """Retorna todas as configurações do router passado por parâmetro."""

        routers = NetworkData.yaml.config_routers['routers']

        for router in routers:
            for name, conf in router.items():
                if name == router_obj.nome:
                    return conf


    @classmethod
    def get_network_interfaces(cls, router_obj):
        """Retorna somente as configurações de interfaces do router passado por parâmetro."""

        router = cls.get_router_config(router_obj)

        return router['network']


# CONTROLLER

class Network(NetworkData):
    
    def __init__(self, router, subnet):
        """Network - Gerencia as interfaces de rede de cada roteador.

        :router: Objeto de Router - obj.
        :subnet: Objeto de Subnet - obj.
        """

        self.router = router
        self.interfaces = Network.declare_interfaces(self, subnet)


    def declare_interfaces(self, subnet):
        """ Instancia as interfaces de cada router. """

        _interfaces = NetworkData.get_network_interfaces(self.router)

        int_list = []
        subnet_name = str()
        subnet_cidr = int()

        for interface in _interfaces:
            name = list(interface.keys())
            name = name[0]

            for line in interface.values():
                full_ip = line['ip']
                
                if full_ip != None:
                    subnet_name, subnet_cidr = full_ip.split('/')

                description = line['description']

            int_list.append(Interface(  name = name, 
                                        description = description, 
                                        full_ip = subnet_name))
        return int_list
        
