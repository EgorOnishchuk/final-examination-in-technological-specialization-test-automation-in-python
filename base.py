from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from logging import debug, exception
from requests import request
from time import sleep
from yaml import safe_load

with open('config.yaml', encoding='UTF-8') as configuration, open('locators.yaml') as locators:
    configuration = safe_load(configuration)
    locators = safe_load(locators)


class BaseAPI:
    """
    Абстрактный интерфейс программирования приложения.
    """
    def __init__(self, url: str = None) -> None:
        """
        Создаёт интерфейс программирования приложения.
        :param url: Универсальный указатель ресурса. При неуказании используется корневой адрес.
        """
        try:
            self.url = url if url is not None else configuration['base_api_url']
        except KeyError:
            exception('Не найден базовый URL в конфигурации проекта')

    def execute_request(self, method: str, parameters: dict = None, body: dict = None, headers: dict = None) -> None:
        """
        Выполняет HTTP запрос к серверу.
        :param method: HTTP метод.
        :param parameters: Аргументы адресной строки.
        :param body: Тело.
        :param headers: Заголовки.
        """
        request(method, self.url, params=parameters, data=body, headers=headers)

    def get_response_json(self, method: str, parameters: dict = None, body: dict = None, headers: dict = None) -> dict:
        """
        Выполняет HTTP запрос к серверу.
        :param method: HTTP метод.
        :param parameters: Аргументы адресной строки.
        :param body: Тело.
        :param headers: Заголовки.
        :return: Тело ответа в формате JSON.
        """
        return request(method, self.url, params=parameters, data=body, headers=headers).json()

    @staticmethod
    def authorize() -> dict | None:
        """
        Авторизует пользователя в системе по его логину и паролю.
        :return: Ключ авторизации, если его удалось получить.
        """
        try:
            body = {
                'username': configuration['user_name'],
                'password': configuration['user_password'],
            }
        except KeyError:
            exception('Не найдены данные пользователя в конфигурации проекта')
            return
        try:
            return request('POST', configuration['base_api_url'], data=body).json()
        except KeyError:
            exception('Структура тела ответа от сервера не соответствует ожидаемой')


class BasePage:
    """
    Абстрактная страница веб-приложения.
    """
    def __init__(self, browser: Chrome, url: str = None) -> None:
        """
        Создаёт абстрактуню страницу.
        :param browser: Настроенный программно-управляемый браузер.
        :param url: Универсальный указатель ресурса. При неуказании используется корневой адрес.
        """
        self.browser = browser
        try:
            self.url = url if url is not None else configuration['base_page_url']
        except KeyError:
            exception('Не найден базовый URL в конфигурации проекта')

    def open(self) -> None:
        """
        Открывает веб-страницу.
        """
        self.browser.get(self.url)
        debug(f'Открыта страница {self.url}')

    def get_element(self, locator: str, waiting: int = 10) -> WebElement:
        """
        Получает HTML элемент по XPath, отводя на ожидание его появления указанное время.
        :param locator: Тип и путь локатора.
        :param waiting: Предельно допустимое время ожидания появления элемента.
        :return: Элемент.
        """
        return WebDriverWait(self.browser, waiting).until(presence_of_element_located((By.XPATH, locator)))

    def get_element_text(self, locator: str, waiting: int = 10) -> str:
        """
        Получает содержание HTML элемента по Xpath, отводя на ожидание его появления указанное время.
        :param locator: Тип и путь локатора.
        :param waiting: Предельно допустимое время ожидания появления элемента.
        :return: Содержание в текстовом виде.
        """
        return self.get_element(locator, waiting).text

    def get_element_css_property(self, locator: str, property_: str, waiting: int = 10) -> str:
        """
        Получает значение CSS свойства HTML элемента по XPath, отводя на ожидание появления HTML элемента указанное
        время.
        :param locator: Путь к элементу.
        :param property_: Имя свойства элемента.
        :param waiting: Предельно допустимое время ожидания появления элемента.
        :return: Значение свойства.
        """
        return self.get_element(locator, waiting).value_of_css_property(property_)

    def get_alert_text(self) -> str:
        """
        Получает содержание уведомления.
        :return: Содержание в текстовом виде.
        """
        return self.browser.switch_to.alert.text

    def fill_input(self, data: str, locator: str, input_name: str) -> None:
        """
        Заполняет поле ввода.
        :param data: Данные к заполнению.
        :param locator: Путь к полю.
        :param input_name: Имя поля ввода в родительном падеже для отладочных целей.
        """
        self.get_element(locator).send_keys(data)
        debug(f'В поле ввода {input_name} введено: {data}')

    def click_button(self, locator: str, button_name: str) -> None:
        """
        Нажимает на кнопку или ссылку.
        :param locator: Путь к кнопке или ссылке.
        :param button_name: Название
        :return: Имя кнопки или ссылки в родительном падеже для отладочных целей.
        """
        self.get_element(locator).click()
        debug(f'Нажата кнопка {button_name}')

    def authorize(self) -> None:
        """
        Авторизует пользователя по имени пользователя и паролю.
        """
        try:
            self.fill_input(configuration['user_name'], locators['user_name_input'], 'логина пользователя')
            self.fill_input(configuration['user_password'], locators['user_password_input'], 'пароля пользователя')
        except KeyError:
            exception('Не найдены данные пользователя в конфигурации проекта')
        try:
            self.click_button(locators['authorization_button'], 'авторизации пользователя')
        except KeyError:
            exception('Не найден XPath к элементу в списке локаторов проекта')
        try:
            sleep(configuration['visual_delay'])
        except KeyError:
            exception('Не найдены данные визуальной задержки в конфигурации проекта')
