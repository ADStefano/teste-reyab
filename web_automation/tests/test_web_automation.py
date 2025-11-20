from unittest.mock import MagicMock

import pytest
import pandas as pd

from web_automation.web_automation import WebAutomation


@pytest.fixture
def mock_config():
    config = {"DEFAULT": {"siteDesafio": "http://teste.com", "downloadFileName": "challenge.xlsx"}}
    return config

@pytest.fixture
def mock_driver():
    mock = MagicMock(name="MockDriver")
    return mock

def test_web_automation_read_file(tmp_path, mock_config, mock_driver):
    """ Teste para validar se o DataFrame é criado com as colunas corretas """

    download_folder = tmp_path / mock_config["DEFAULT"]["downloadFileName"]
    test_data = pd.DataFrame({
        "First Name": ["John", "Jane"],
        "Last_name": ["Darksouls", "Sekiro"],
        "Address": ["Rua dos bobos nº 0", "Av. Paulista"],
        "EMAIL": ["john@darksouls.com", "jane@sekiro.com"],
        "  Company ": ["FromSoftware", "DoSoftware"],
        "Phone  ": ["123456789", "987654321"],
        " ROle in Company ": ["Developer", "Designer"]
    })
    
    test_data.to_excel(download_folder, index=False)

    web_auto = WebAutomation(config_parser=mock_config, driver=mock_driver, download_folder=tmp_path)
    df = web_auto._read_file()

    assert not df.empty
    assert "first_name" in df.columns
    assert "last_name" in df.columns
    assert "address" in df.columns
    assert "email" in df.columns
    assert "company" in df.columns
    assert "phone" in df.columns
    assert "role_in_company" in df.columns

def test_web_automation_read_file_file_not_found(tmp_path, mock_config, mock_driver):
    """ Teste para validar se a exception correta é levantada """

    web_auto = WebAutomation(config_parser=mock_config, driver=mock_driver, download_folder=tmp_path)
    
    with pytest.raises(FileNotFoundError):
        web_auto._read_file()

def test_web_automation_get_time(tmp_path, mock_config, mock_driver):
    """ Teste para validar se o regex funciona corretamente """

    web_auto = WebAutomation(config_parser=mock_config, driver=mock_driver, download_folder=tmp_path)

    fake_time = MagicMock()
    fake_time.text = "Your success rate is 100 in 123 milliseconds"

    web_auto._driver_wait = MagicMock()
    web_auto._driver_wait.until.return_value = fake_time
    elapsed_time = web_auto._get_time()

    assert elapsed_time == "123"