from subprocess import run, PIPE


class CommandLineInterface:
    def __init__(self, application: str) -> None:
        """
        Создаёт интерфейс командной строки для работы с консольным приложением.
        :param application: Имя приложения, по которому оно вызывается из командной строки.
        """
        self.application = application

    def get_output(self, arguments: str = None) -> str:
        """
        Получает стандартный поток вывода консольной команды.
        :param arguments: Аргументы команды.
        :return: Текст стандартного потока вывода.
        """
        return run(f'{self.application} {arguments if arguments is not None else ""}', shell=True, stdout=PIPE,
                   encoding='UTF-8').stdout

    def is_text_in_output(self, text: str, arguments: str = None) -> bool:
        """
        Проверяет наличие текста в выводе консольной команды.
        :param text: Текст, который должен присутствовать в выводе в любом виде, в том числе встречаться в составе других
                     слов.
        :param arguments: Аргументы команды.
        :return: True, если текст присутствует в выводе команды, и False - если нет.
        """
        return text in run(f'{self.application} {arguments if arguments is not None else ""}', shell=True,
                           stdout=PIPE, encoding='UTF-8').stdout
