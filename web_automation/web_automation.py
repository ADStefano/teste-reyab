import os
import re
import time
import shutil
import logging

import pandas as pd
from pathlib import Path
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebAutomation:
    """ Classe reponsável pela automação do teste """


    def __init__(self, config_parser: ConfigParser, driver: webdriver.Chrome, download_folder: Path) -> None:

        self._logger = logging.getLogger(__name__)
        self._url = config_parser["DEFAULT"]["siteDesafio"]

        self._download_folder = download_folder
        self._download_file_name = config_parser["DEFAULT"]["downloadFileName"]

        self._driver = driver
        self._driver_wait = WebDriverWait(self._driver, 5)

    def _download_file(self) -> None:
        """ Procura o botão de download e baixa o arquivo"""

        # self._logger.info("Baixando o arquivo")

        download_bttn = self._driver_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href$='{self._download_file_name}']")))
        download_bttn.click()

    def _download_wait(self, timeout: int, nfiles: int) -> int:
        """ Verifica se o arquivo foi baixado """

        seconds = 0
        dl_wait = True

        while dl_wait and seconds < timeout:
            time.sleep(0.5)
            dl_wait = False
            files = os.listdir(str(self._download_folder))

            if nfiles and len(files) != nfiles:
                dl_wait = True

            for fname in files:
                if fname.endswith('.crdownload'):
                    dl_wait = True

            seconds += 1

        return seconds

    def _read_file(self) -> pd.DataFrame:
        """ Lê o arquivo baixado """

        # self._logger.info("Criando DataFrame")
        file_path = self._download_folder / self._download_file_name

        if not file_path.exists():
            raise FileNotFoundError(f"O arquivo {file_path} não foi encontrado.")
        
        df = pd.read_excel(str(file_path))

        # self._logger.info(f"Colunas do DataFrame {df.columns.tolist()}")
        # self._logger.info("Ajustando nomes das colunas")
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        return df

    def _start_challange(self) -> None:
        """ Inicia o desafio """

        # self._logger.info("Iniciando o desafio")
        start_bttn = self._driver_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Start']")))
        start_bttn.click()
    
    def _fill_form(self, df: pd.DataFrame) -> None:
        """ Preenche e envia o formulário com os dados do arquivo """

        # self._logger.info("Preenchendo o formulário")

        for index, row in enumerate(df.itertuples()):

            try:

                # self._logger.info(f"Preenchendo formulário nª: {index + 1} {row['first_name']}")

                name = self._driver_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-reflect-name='labelFirstName']")))
                last_name = self._driver_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-reflect-name='labelLastName']")))
                address = self._driver_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-reflect-name='labelAddress']")))
                email = self._driver_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-reflect-name='labelEmail']")))
                company = self._driver_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-reflect-name='labelCompanyName']")))
                phone = self._driver_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-reflect-name='labelPhone']")))
                role = self._driver_wait.until(EC.presence_of_element_located((By.XPATH, "//input[@ng-reflect-name='labelRole']")))

                name.send_keys(row.first_name)
                last_name.send_keys(row.last_name)
                address.send_keys(row.address)
                email.send_keys(row.email)
                company.send_keys(row.company_name)
                phone.send_keys(str(row.phone_number))
                role.send_keys(row.role_in_company)

                # self._logger.info("Enviando formulário")
                submit_bttn = self._driver_wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
                submit_bttn.click()

            except Exception as e:
                # self._logger.error(f"Erro ao preencher o formulário nª {index + 1}: {e}", exc_info=True)
                raise e(f"Erro ao preencher o formulário nª {index + 1}: {e}")

    def _get_time(self) -> str:
        """ Retorna o tempo do desafio """

        time_message = self._driver_wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "message2")))
        time_text = time_message.text
        submission_time = re.search(r"in\s+(\d+)\s+milliseconds", time_text)

        if not submission_time:
            raise ValueError("Não foi possível extrair o tempo de submissão.")

        return submission_time.group(1)


    def execute(self) -> None:
        """ Método executor da classe """

        try:

            self._driver.get(self._url)
            self._download_file()
            download_time = self._download_wait(10, 1)
            # self._logger.info(f"Arquivo baixado em {download_time} segundos")

            df = self._read_file()
            self._start_challange()
            self._fill_form(df)

            submission_time = self._get_time()
            self._logger.info(submission_time)

        except Exception as e:
            # self._logger.error(f"Erro ao executar automação: {e}", exc_info=True)
            raise e

        finally:
            self._driver.quit()

            try:
                if self._download_folder.exists():
                    # self._logger.info("removendo a pasta tmp")
                    shutil.rmtree(str(self._download_folder))

            except Exception as e:
                raise e(f"Erro ao remover arquivo baixado: {e}", exc_info=True)
