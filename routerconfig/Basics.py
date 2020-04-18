"""Cria as configuracoes basicas de cada roteador."""

from .Yaml import YamlReader


class Basics:

    def __init__(self, router):
        """Basics - Cria as configuracoes basicas de cada roteador.

        :router: Objeto de Router.
        """

        self.router = router

    # Leitura dos dados do campo basics de routers.yaml
    basic_parameters = YamlReader().basic


    @classmethod
    def get_default_password(cls):
        """Retorna senha definida em basics de routers.yaml."""
        
        _position = cls.basic_parameters[2]
        
        return _position['password']


    @classmethod
    def get_default_server_ip(cls):
        """Retorna server_ip definido em basics de routers.yaml."""
        
        _position = cls.basic_parameters[1]
        
        return _position['server_ip']


    @classmethod
    def get_script_file(cls):
        """Retorna leitura do arquivo de script definido em basics de routers.yaml, no formato list."""
        
        basics = open('router-config/cisco/basics.ios', 'r')
        cls.basics_content = basics.readlines()

        return cls.basics_content


    @classmethod
    def replace_vars(cls, itter_list, pattern, replace):
        """Funcao generica para substituicao de padrao de string dentro de uma lista."""

        for index, line in enumerate(itter_list):
            itter_list[index] = line.replace(pattern, replace)

        return itter_list


    def configure_basics_in_routers(self):
        """Adiciona os itens bascicos de basics.ios em cada roteador."""
    
        basics_script = Basics.get_script_file()
        
        # Alteracao do nome e senha do router no script
        basics_script = Basics.replace_vars(itter_list=basics_script, pattern='{%hostname%}', replace=self.router.nome)
        basics_script = Basics.replace_vars(itter_list=basics_script, pattern='{%password%}', replace=Basics.get_default_password())

        _path = f'router-config/cisco/{self.router.nome}.ios'

        router_configfile = open(_path, 'w')

        # Gravacao dos dados nos arquivos de cada router em cisco/
        try:
            for line in basics_script:
                router_configfile.write(line)
            
            return f'BASICS: Arquivo de configuracao de {self.router.nome} criado com sucesso em {_path}.'
        
        except: f'BASICS: Erro na configuracao do arquivo de {self.router.nome} em {_path}!'

        router_configfile.close()