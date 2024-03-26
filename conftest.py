from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytest import fixture
from yaml import safe_load

with open('config.yaml', encoding='UTF-8') as file:
    configuration = safe_load(file)


@fixture()
def browser() -> Chrome:
    """
    Создаёт программно-управляемый браузер Chrome.
    :return: Браузер.
    """
    browser = Chrome(ChromeOptions(), Service(ChromeDriverManager().install()))
    browser.implicitly_wait(configuration['implicit_delay'])
    browser.maximize_window()
    yield browser
    browser.quit()
