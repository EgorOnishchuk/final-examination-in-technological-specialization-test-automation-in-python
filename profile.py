from base import BaseAPI


class ProfileAPI(BaseAPI):
    """
    Программный интерфейс профиля.
    """
    def get_user_profile(self, token: str) -> dict | None:
        """
        Возвращает профиль пользователя.
        :param token: Ключ авторизации.
        :return: Профиль в формате JSON.
        """
        headers = {
            'X-Auth-Token': token,
        }
        return self.get_response_json('GET', headers=headers)
