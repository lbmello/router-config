from .routerconfig import Router
from .routerconfig import YamlReader
from .routerconfig import Basics
from .routerconfig import Telnet
from .routerconfig import NetworkData, Network
from .routerconfig import Scope
from .routerconfig import Subnet
from .routerconfig.Utils import debug_mode

# Leitura dos arquivos e instância dos roteadores
yaml = YamlReader()

def create_routers():
    """ Lê os dados no arquivo YAML e instancia cada roteador."""
    router_objects = []

    for router in yaml.routers:
        for name, conf in router.items():
            router_objects.append(Router(   nome=name,
                                            gns_port=conf['gns_port'],
                                            ios=conf['ios'], 
                                            networks=conf['network'],
                                            scope=conf['scope'], 
                                            script=conf['script_file']))
    return router_objects

# Roteadores sendo instanciados
routers_objs = create_routers()

# TODO: ALTERAR PARA MODO RECURSIVO, LENDO CADA ESCOPO GLOBAL DO ARQUIVO
# Instância dos objetos de scope
scope_objs = []

for scope_name in NetworkData.get_global_name():
    scope_objs.append(Scope(scope_name))

# Instância das subnets de cada escopo

subnets = []

for scope_obj in scope_objs:
    for scope_name in scope_obj.subnets:
        _name, _mask = scope_name.split('/')
        
        _sn_obj = Subnet(name=_name, local_mask=_mask, local_address=scope_obj.get_subnet())
        _sn_obj.ip_calculator()

        subnets.append(_sn_obj)
    
        debug_mode(_sn_obj.get_debug())


'''norte = scope_objs[0]
#norte.subnet_calculator()

sul = scope_objs[1]
#sul.subnet_calculator()

# TODO: CADA LINHA DE SUBNET DEVERÁ GERAR UM OBJ COM O local_mask DEFINIDO PARA A SUBNET NO ARQUIVO
subnet_norte = Subnet(name=norte.name, local_mask=22, local_address=norte.get_subnet())
subnet_norte.ip_calculator()
subnet_sul = Subnet(name=sul.name, local_mask=22, local_address=sul.get_subnet())
subnet_sul.ip_calculator()
'''

# Execução dos processos em cada router
for router in routers_objs:
    debug_mode('')
    debug_mode(f'***** Roteador {router.nome} *****')
    
    # Aplica as configurações básicas nos scripts dos routers
    generate_basics_script = Basics(router)
    basics_apply = generate_basics_script.configure_basics_in_routers()
    debug_mode(basics_apply)

    # TODO: VERIFICAR COMO CRIAR LÓGICA RECURSIVA, CONFORME MENCIONADO ACIMA
    
    # TODO: ALTERAR PARA LEITURA DO CIDR DE CADA SUBNET, FILTRAR SE O ROTEADOR TEM ALGUM IP COM NOME IGUAL AS INSTÂNCIAS DE SUBNET DECLARADAS ACIMA

    for sn in subnets:

        if router.scope == 'NORTE':
            nw_norte = Network(router, sn.name)
            for inter in nw_norte.interfaces:
                # TODO: PEGAR LEITURA DE CADA INTERFACE DO ROUTER NO ARQUIVO YAML, COMPARAR O NOME E PEGAR IP DESSA SUBNET
                
                if inter.full_ip == sn.name:

                    debug_mode(f'ROUTER_CONFIG: Interface {inter.name} rererente ao roteador {nw_norte.router.nome} sendo configurada')

                    _ip = sn.get_ip()
                    _mask = sn.local_mask

                    inter.set_ip(_ip, _mask)
                    inter.no_shutdown()
                    inter.write_changes(router)

        if router.scope == 'SUL':
            nw_sul = Network(router, sn.name)
            for inter in nw_sul.interfaces:

                if inter.full_ip == sn.name:

                    debug_mode(f'ROUTER_CONFIG: Interface {inter.name} rererente ao roteador {nw_sul.router.nome} sendo configurada')

                    _ip = sn.get_ip()
                    _mask = sn.local_mask

                    inter.set_ip(_ip, _mask)
                    inter.no_shutdown()
                    inter.write_changes(router)

    
    # Telnet
    telnet_session = Telnet(router)
    debug_mode(telnet_session.run_script())
    debug_mode(telnet_session.session_close())
