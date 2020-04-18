
from .routerconfig import Basics
from .routerconfig import NetworkData, Network
from .routerconfig import Router
from .routerconfig import Scope
from .routerconfig import Subnet
from .routerconfig import Telnet
from .routerconfig.Utils import debug_mode
from .routerconfig import YamlReader


def create_routers():
    """ Le os dados no arquivo YAML e instancia os objetos de cada roteador."""
    
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

# Leitura do arquivo YAML
yaml = YamlReader()


# Roteadores sendo instanciados
routers_objs = create_routers()


# Instancia dos objetos de escopo
scope_objs = []

for scope_name in NetworkData.get_global_name():
    scope_objs.append(Scope(scope_name))

# Instancia das subnets de cada escopo
subnets = []

for scope_obj in scope_objs:
    for scope_name in scope_obj.subnets:
        _name, _mask = scope_name.split('/')
        
        _sn_obj = Subnet(name=_name, local_mask=_mask, local_address=scope_obj.get_subnet())
        _sn_obj.ip_calculator()

        subnets.append(_sn_obj)
    
        debug_mode(_sn_obj.get_debug())


# Execucao dos processos em cada router
for router in routers_objs:
    debug_mode('')
    debug_mode(f'***** Roteador {router.nome} *****')
    
    # Aplica as configuracoess basicas nos scripts dos routers
    generate_basics_script = Basics(router)
    basics_apply = generate_basics_script.configure_basics_in_routers()
    debug_mode(basics_apply)
    
    for subnet in subnets:        
        nw = Network(router, subnet.name)
        for interface in nw.interfaces:           
            if interface.full_ip == subnet.name:

                debug_mode(f'ROUTER_CONFIG: Interface {interface.name} rererente ao roteador {nw.router.nome} sendo configurada')

                _ip = subnet.get_ip()
                _mask = subnet.local_mask

                # Configuracoes da interface de rede
                interface.set_ip(_ip, _mask)
                interface.no_shutdown()
                interface.write_changes(router)

   
    # Telnet
    telnet_session = Telnet(router)

    debug_mode(telnet_session.run_script())
    debug_mode(telnet_session.session_close())
