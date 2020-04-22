"""Modulo generico de funcoes."""


from .Yaml import YamlReader

yaml_obj = YamlReader()
debug = yaml_obj.get_debug()
exit_path = yaml_obj.get_exit_file()


def debug_mode(info):
    """ Quando o variavel debug está setada em True, este metodo printa as saedas de cada passo em tela."""

    exit_file = open(exit_path, 'a+')

    # Grava dado no arquivo
    exit_file.write(f'{info}\n')

    exit_file.close()

    if debug == True:
        # Exibe saida no shell
        print(info)
