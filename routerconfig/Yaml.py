""" Modulo que le arquivo routers.yaml."""

import yaml

from .Router import Router


class YamlReader:

    routers_yaml = open('/home/lucas/Documents/GitHub/router-config/routers.yaml', 'r')
    config_routers = yaml.load(routers_yaml, Loader=yaml.FullLoader)

    def __init__(self):
        """ YamlReader: Le dados de routers.yaml e separa as sessoes do arquivo."""

        self.basic = YamlReader.config_routers['basic']
        self.routers = YamlReader.config_routers['routers']
        self.networks = YamlReader.config_routers['networks']

        YamlReader.routers_yaml.close()
