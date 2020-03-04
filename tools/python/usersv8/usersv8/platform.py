from . import UsersClient
from .utils import (
    argparse,
    is_amd64_sys,
    is_deb_based_linux,
    is_osx,
    is_rpm_based_linux,
)


class PlatformDownloadHelper(UsersClient):
    """
    Класс реализует функции помощника доступа к файлам
    в составе дистрибутива платформы 1С:Предприятие
    """

    _sys_type_win = "win"
    _sys_type_deb = "deb"
    _sys_type_rpm = "rpm"
    _sys_type_osx = "osx"
    _sys_type_win64 = "win64"
    _sys_type_deb64 = "deb64"
    _sys_type_rpm64 = "rpm64"

    def __init__(self, file):
        super().__init__()
        self.file = file

    # Служебные процедуры и функции

    def _get_project_name(self, version: str or None = None):
        """Получает имя проекта по версии"""
        if version is None:
            version = "8.3"
        return "Platform" + version[0:3].replace(".", "")

    def _get_project(self, version: str or None = None):
        """Получает проект по версии"""
        return self.get_project(nick=self._get_project_name(version=version))

    def _get_sys_type(self):

        """
        Получение тип текущей операционной системы
        в контексте доступных дистрибутивов
        """

        sys_type = None

        if is_deb_based_linux():
            if is_amd64_sys():
                sys_type = self._sys_type_deb64
            else:
                sys_type = self._sys_type_deb
        elif is_rpm_based_linux():
            if is_amd64_sys():
                sys_type = self._sys_type_rpm64
            else:
                sys_type = self._sys_type_rpm
        elif is_osx():
            sys_type = self._sys_type_osx
        else:
            if is_amd64_sys():
                sys_type = self._sys_type_win64
            else:
                sys_type = self._sys_type_win

        return sys_type

    # Скачивание файла платформы по имени

    def _download_file(self, name: str, version: str or None = None) -> bytes:
        """Скачивает файл версии проекта по имени"""
        users_project = self._get_project(version=version)
        if version is None:
            # TODO сделать нормальную обработку возможного исключения
            users_version = self.get_versions(project=users_project)[0]
        else:
            users_version = self.get_version(project=users_project, version=version)
        file_ = self.get_file(version=users_version, name=name)
        return self.download(file_=file_, out_file=self.file)

    # Скачивание типа дистрибутива

    def get_tc(self, version: str or None = None) -> bytes:
        """
        Тонкий клиент 1С:Предприятия
        """
        sys_type = self._get_sys_type()
        if sys_type == self._sys_type_deb:
            f = self.get_tc_deb
        elif sys_type == self._sys_type_deb64:
            f = self.get_tc_deb64
        elif sys_type == self._sys_type_rpm:
            f = self.get_tc_rpm
        elif sys_type == self.get_tc_rpm64:
            f = self.get_tc_rpm64
        elif sys_type == self._sys_type_win:
            f = self.get_tc_win
        elif sys_type == self._sys_type_win64:
            f = self.get_tc_win64
        elif sys_type == self._sys_type_osx:
            f = self.get_tc_osx
        else:
            raise Exception("Не удалось определить тип дистрибутива")

        return f(version=version)

    def get_client(self, version: str or None = None) -> bytes:
        """
        Клиент 1С:Предприятия
        Технологическая платформа 1С:Предприятия
        """
        sys_type = self._get_sys_type()
        if sys_type == self._sys_type_deb:
            f = self.get_client_deb
        elif sys_type == self._sys_type_deb64:
            f = self.get_client_deb64
        elif sys_type == self._sys_type_rpm:
            f = self.get_client_rpm
        elif sys_type == self.get_tc_rpm64:
            f = self.get_client_rpm64
        elif sys_type == self._sys_type_win:
            f = self.get_client_win
        elif sys_type == self._sys_type_win64:
            f = self.get_client_win64
        elif sys_type == self._sys_type_osx:
            f = self.get_client_osx
        else:
            raise Exception("Не удалось определить тип дистрибутива")

        return f(version=version)

    def get_server(self, version: str or None = None) -> bytes:
        """
        Cервер 1С:Предприятия
        """
        sys_type = self._get_sys_type()
        if sys_type == self._sys_type_deb:
            f = self.get_server_deb
        elif sys_type == self._sys_type_deb64:
            f = self.get_server_deb64
        elif sys_type == self._sys_type_rpm:
            f = self.get_server_rpm
        elif sys_type == self.get_tc_rpm64:
            f = self.get_server_rpm64
        elif sys_type == self._sys_type_win:
            f = self.get_client_win
        elif sys_type == self._sys_type_win64:
            f = self.get_server_win64
        else:
            raise Exception("Не удалось определить тип дистрибутива")

        return f(version=version)

    # Скачивание дистрибутива

    def get_tc_win(self, version: str or None = None) -> bytes:
        """
        Тонкий клиент 1С:Предприятия для Windows
        """
        n = "Тонкий клиент 1С:Предприятия для Windows"
        return self._download_file(name=n, version=version)

    def get_tc_win64(self, version: str or None = None) -> bytes:
        """
        Тонкий клиент 1С:Предприятие (64-bit) для Windows
        """
        n = "Тонкий клиент 1С:Предприятие (64-bit) для Windows"
        return self._download_file(name=n, version=version)

    def get_tc_deb(self, version: str or None = None) -> bytes:
        """
        Тонкий клиент 1С:Предприятия для DEB-based Linux-систем
        """
        n = "Тонкий клиент 1С:Предприятия для DEB-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_tc_deb64(self, version: str or None = None) -> bytes:
        """
        Тонкий клиент 1С:Предприятия (64-bit) для DEB-based Linux-систем
        """
        n = "Тонкий клиент 1С:Предприятия (64-bit) для DEB-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_tc_rpm(self, version: str or None = None) -> bytes:
        """
        Тонкий клиент 1С:Предприятия для RPM-based Linux-систем
        """
        n = "Тонкий клиент 1С:Предприятия для RPM-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_tc_rpm64(self, version: str or None = None) -> bytes:
        """
        Тонкий клиент 1С:Предприятия (64-bit) для RPM-based Linux-систем
        """
        n = "Тонкий клиент 1С:Предприятия (64-bit) для RPM-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_tc_osx(self, version: str or None = None) -> bytes:
        """
        Тонкий клиент 1С:Предприятия для OS X
        """
        n = "Тонкий клиент 1С:Предприятия для OS X"
        return self._download_file(name=n, version=version)

    def get_client_win(self, version: str or None = None) -> bytes:
        """
        Технологическая платформа 1С:Предприятия для Windows
        """
        n = "Технологическая платформа 1С:Предприятия для Windows"
        return self._download_file(name=n, version=version)

    def get_client_win64(self, version: str or None = None) -> bytes:
        """
        Технологическая платформа 1С:Предприятия (64-bit) для Windows
        """
        n = "Технологическая платформа 1С:Предприятия (64-bit) для Windows"
        return self._download_file(name=n, version=version)

    def get_client_deb(self, version: str or None = None) -> bytes:
        """
        Клиент 1С:Предприятия для DEB-based Linux-систем
        """
        n = "Клиент 1С:Предприятия для DEB-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_client_deb64(self, version: str or None = None) -> bytes:
        """
        Клиент 1С:Предприятия (64-bit) для DEB-based Linux-систем
        """
        n = "Клиент 1С:Предприятия (64-bit) для DEB-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_client_rpm(self, version: str or None = None) -> bytes:
        """
        Клиент 1С:Предприятия для RPM-based Linux-систем
        """
        n = "Клиент 1С:Предприятия для RPM-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_client_rpm64(self, version: str or None = None) -> bytes:
        """
        Клиент 1С:Предприятия (64-bit) для RPM-based Linux-систем
        """
        n = "Клиент 1С:Предприятия (64-bit) для RPM-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_client_osx(self, version: str or None = None) -> bytes:
        """
        Клиент 1С:Предприятия для OS X
        """
        n = "Клиент 1С:Предприятия для OS X"
        return self._download_file(name=n, version=version)

    def get_server_win64(self, version: str or None = None) -> bytes:
        """
        Cервер 1С:Предприятия (64-bit) для Windows
        """
        n = "Cервер 1С:Предприятия (64-bit) для Windows"
        return self._download_file(name=n, version=version)

    def get_server_deb(self, version: str or None = None) -> bytes:
        """
        Cервер 1С:Предприятия для DEB-based Linux-систем
        """
        n = "Cервер 1С:Предприятия для DEB-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_server_deb64(self, version: str or None = None) -> bytes:
        """
        Cервер 1С:Предприятия (64-bit) для DEB-based Linux-систем
        """
        n = "Cервер 1С:Предприятия (64-bit) для DEB-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_server_rpm(self, version: str or None = None) -> bytes:
        """
        Cервер 1С:Предприятия для RPM-based Linux-систем
        """
        n = "Cервер 1С:Предприятия для RPM-based Linux-систем"
        return self._download_file(name=n, version=version)

    def get_server_rpm64(self, version: str or None = None) -> bytes:
        """
        Cервер 1С:Предприятия (64-bit) для RPM-based Linux-систем
        """
        n = "Cервер 1С:Предприятия (64-bit) для RPM-based Linux-систем"
        return self._download_file(name=n, version=version)


def parser():

    parser = argparse.ArgumentParser(
        prog="PlatformDownloadHelper", description="Помощник скачивания платформы"
    )

    subparsers = parser.add_subparsers(dest="command", help="Команды:")
    subparsers.required = True

    for cmd in ["tc", "client", "server", "server_deb64"]:

        s = subparsers.add_parser(cmd)
        s.add_argument(
            "--version", dest="version", help="Версия", type=str, required=False
        )

        s.add_argument(
            "--out-file",
            dest="out_file",
            help="Файл результат",
            type=str,
            required=True,
        )

        s.add_argument(
            "--username",
            dest="users_username",
            help="Пользователь users.v8.1c.ru",
            required=True,
        )

        s.add_argument(
            "--password",
            dest="users_password",
            help="Пароль users.v8.1c.ru",
            type=str,
            required=True,
        )

    return parser


def main():

    args = parser().parse_args()

    file = open(args.out_file, "wb")
    helper = PlatformDownloadHelper(file)
    helper.authorize(username=args.users_username, password=args.users_password)

    if args.command == "tc":
        helper.get_tc(args.version)
    elif args.command == "client":
        helper.get_client(args.version)
    elif args.command == "server":
        helper.get_server(args.version)
    elif args.command == "server_deb64":
        helper.get_server_deb64(args.version)
    else:
        raise Exception("Не предполагаемая команда")


if __name__ == "__main__":

    main()
