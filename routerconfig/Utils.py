"""Modulo generico de funcoes."""


from .Yaml import YamlReader

yaml_obj = YamlReader()
debug = yaml_obj.get_debug()


def debug_mode(info):
    """ Quando o variável debug está setada em True, este método printa as saídas de cada passo em tela."""

    if debug == True:
        
        print(info)
        
        return True
