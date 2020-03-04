from .responses import (
    UsersFile,
    UsersFileList,
    UsersProject,
    UsersProjectList,
    UsersVersion,
    UsersVersionList,
)
from .utils import html, requests


class UsersClient(object):
    """Класс реализующий доступ к сервису user"""

    def __init__(self):
        self._session: requests.Response = None

    def authorize(self, username: str, password: str):

        """
        Авторизация в сервисе по имени и паролю
        Параметры:
            username: str: имя пользователя
            password: str: пароль
        """

        s = requests.Session()
        s.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) \
                Gecko/20100101 Firefox/45.0"
            }
        )
        r = s.get("https://releases.1c.ru")
        r.raise_for_status()

        # Поиск мохнатого элемента,
        # значение его атрибута нужно для запроса авторизации

        tree = html.fromstring(r.text)
        exec_node = tree.xpath('//input[@name="execution"]')

        if not exec_node:
            raise Exception("Не найден предполагаемый тег")

        data = {
            "_eventId": "submit",
            "username": username,
            "password": password,
            "execution": exec_node[0].value,
            "inviteCode": "",
        }

        r = s.post("https://login.1c.ru/login", data=data)
        r.raise_for_status()

        self._session = s

    def get_projects(self, hide_na_programs: bool = True) -> UsersProjectList:
        """
        Получить список проектов
        hide_na_programs - скрыть недоступные
        """

        url = "https://releases.1c.ru/total?"
        params = {"hideUnavailablePrograms": hide_na_programs}

        r = self._session.get(url, params=params)
        r.raise_for_status()

        return UsersProjectList(r.text)

    def get_versions(self, project: UsersProject) -> UsersVersionList:
        """Получить список версий проекта"""

        r = self._session.get("https://releases.1c.ru" + project.url)
        r.raise_for_status()

        return UsersVersionList(r.text)

    def get_files(self, version: UsersVersion) -> UsersFileList:
        """Получить список файлов версии"""

        r = self._session.get("https://releases.1c.ru" + version.url)
        r.raise_for_status()

        return UsersFileList(r.text)

    def get_project(self, nick: str) -> UsersProject:
        """Получение проекта по наименованию"""
        for p in self.get_projects():
            if p.nick == nick:
                return p
        return None

    def get_version(self, project: UsersProject, version: str) -> UsersVersion:
        """Получение версии по номеру"""
        for v in self.get_versions(project):
            if v.version == version:
                return v

    def get_file(self, version: UsersVersion, **kwargs) -> UsersFile:
        """
        Получение файла по параметрам
        Параметры:
        version: UsersVersion
        Параметры поиска:
        name
        file_name
        file_short_name
        """
        name = kwargs.get("name")
        file_name = kwargs.get("file_name")
        file_short_name = kwargs.get("file_short_name")

        for f in self.get_files(version):
            if name is not None and f.name == name:
                return f
            if file_name is not None and f.file_name == file_name:
                return f
            if file_short_name is not None and f.file_short_name == file_short_name:
                return f

    def download(self, file_: UsersFile, out_file) -> bytes:

        r = self._session.get("https://releases.1c.ru" + file_.url)
        r.raise_for_status()

        links = file_.get_links(r.text)
        if not links:
            raise Exception("Не найдены ссылки")

        chunk_size = 1024 * 1024
        with self._session.get(links[0], stream=True) as file_resp:
            file_resp.raise_for_status()
            for chunk in file_resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    out_file.write(chunk)
