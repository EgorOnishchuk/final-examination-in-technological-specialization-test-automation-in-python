from logging import info
from yaml import safe_load
from profile import ProfileAPI
from posts import PostsPage
from command_line_interface import CommandLineInterface

with open('config.yaml', encoding='UTF-8') as file:
    configuration = safe_load(file)


class Test:
    """
    Тестирование веб-приложения.
    """
    TESTS_NAMES = (
        'профиля пользователя',
        'описания',
        'уязвимостей',
    )

    def test_user_profile(self) -> None:
        """
        Проверяет соответствие авторизационных данных пользователя данным его профиля.
        """
        info(f'Тестирование {Test.TESTS_NAMES[0]} начато')
        profile_api = ProfileAPI(configuration['profile_api_url'])
        user = profile_api.authorize()
        profile = profile_api.get_user_profile(user['token'])
        assert all([
            user['id'] == profile['id'],
            user['username'] == profile['username'],
        ])
        info(f'Тестирование {Test.TESTS_NAMES[0]} завершено')

    def test_about(self, browser) -> None:
        """
        Проверяет возможность открытия и вёрстку страницы описания.
        :param browser: Программно-управляемый браузер.
        """
        info(f'Тестирование {Test.TESTS_NAMES[1]} начато')
        posts_page = PostsPage(browser)
        posts_page.open()
        posts_page.authorize()
        assert posts_page.get_about_layout() == '64px'
        info(f'Тестирование {Test.TESTS_NAMES[1]} завершено')

    def test_vulnerabilities(self) -> None:
        """
        Проверяет наличие уязвимостей сайта.
        """
        info(f'Тестирование {Test.TESTS_NAMES[2]} начато')
        assert CommandLineInterface('nikto').is_text_in_output('0 error(s)', f'-h {configuration["base_page_url"]} '
                                                               '-ssl -Tuning 4')
