from logging import exception
from yaml import safe_load
from base import BasePage

with open('config.yaml', encoding='UTF-8') as configuration, open('locators.yaml') as locators:
    configuration = safe_load(configuration)
    locators = safe_load(locators)


class PostsPage(BasePage):
    """
    Страница публикаций.
    """
    def get_about_layout(self) -> str | None:
        """
        Проверяет верстку страницы описания.
        :return: Размер шрифта заголовка описания.
        """
        try:
            self.click_button(locators['about_link'], 'описания')
            return self.get_element_css_property(locators['about_title'], 'font-size')
        except KeyError:
            exception('Не найден XPath к элементу в списке локаторов проекта')
