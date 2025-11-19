from configparser import ConfigParser
from pathlib import Path

def load_config() -> ConfigParser:
    """ Carrega a configuração do arquivo INI """

    config_parser = ConfigParser()
    config_file = Path("config.ini")

    if not config_file.exists():
        raise FileNotFoundError("Arquivo de configuração 'config.ini' não encontrado.")
    
    config_parser.read(config_file)
    required_keys = ["siteDesafio", "downloadFileName"]

    for key in required_keys:
        if key not in config_parser["DEFAULT"]:
            raise KeyError(f"Chave obrigatória ausente: {key}")


    return config_parser