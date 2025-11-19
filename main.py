import logging
from web_automation.factory import web_automation_factory

logging.basicConfig(level=logging.INFO,format="[%(asctime)s] [%(levelname)s]: %(message)s")

if __name__ == "__main__":

    try:
    
        web_automation = web_automation_factory()
        web_automation.execute()

    except Exception as e:
        logging.error(f"Erro ao iniciar a automação: {e}")
        raise e