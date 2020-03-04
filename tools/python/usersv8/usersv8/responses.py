from .utils import html, os, urlparse


class UsersParseError(Exception):
    pass


class UsersProjectList(list):
    """Представление списка проектов"""

    def __init__(self, total_response: str):
        tree = html.fromstring(total_response)
        for container in tree.find_class("projects-list-container"):
            for project in container.xpath("//*[@parent-group]"):
                self.append(UsersProject(project))


class UsersProject(object):
    """Представление элемента списка проектов"""

    def __init__(self, project: html.HtmlElement):
        self.name = None
        self.nick = None
        self.url = None
        self.actual_version = None
        self.actual_version_url = None
        # Наименование проекта
        for name_column in project.find_class("nameColumn"):
            for link in name_column.xpath("a"):
                self.name = link.text
                self.url = link.attrib.get("href")
        # Актуальная версия
        for ver_column in project.find_class("actualVersionColumn"):
            for link in ver_column.xpath("a"):
                self.actual_version = link.text
                self.actual_version_url = link.attrib.get("href")
        # Прочее
        if self.url:
            arr = self.url.split("/")
            if len(arr) == 3:
                self.nick = arr[2]


class UsersVersionList(list):
    """Представление списка версий проекта"""

    def __init__(self, versions_response: str):
        tree = html.fromstring(versions_response)
        try:
            versions_table = tree.get_element_by_id("versionsTable")
        except KeyError:
            return
        # Строки версий
        for version in versions_table.xpath("tbody/tr"):
            self.append(UsersVersion(version))


class UsersVersion(object):
    """Представление элемента списка версий проекта"""

    def __init__(self, version: html.HtmlElement):
        self.version = None
        self.date = None
        self.url = None
        self.for_versions = []
        # Номер версии
        for ver_column in version.find_class("versionColumn"):
            for link in ver_column.xpath("a"):
                self.version = link.text.strip()
                self.url = link.attrib.get("href")
        # Дата
        for date_column in version.find_class("dateColumn"):
            self.date = date_column.text.strip()
        # Для версий
        for prev_column in version.find_class("previousVersionsColumn"):
            prev_ver = prev_column.text.strip()
            for version in prev_ver.split(","):
                if version:
                    self.for_versions.append(version.strip())


class UsersFileList(list):
    """Представление списка файлов"""

    def __init__(self, files_response: str):
        tree = html.fromstring(files_response)
        for container in tree.find_class("files-container"):
            for file_ in container.find_class("formLine"):
                try:
                    self.append(UsersFile(file_))
                except UsersParseError:
                    pass


class UsersFile(object):
    """Представление файла"""

    def __init__(self, file_: html.HtmlElement):
        self.name = None
        self.url = None
        self.file_path = None
        self.file_name = None
        self.file_short_name = None
        # Ссылка на файл
        for link in file_.xpath("a"):
            self.name = link.text.strip()
            self.url = link.attrib.get("href")
        # Не удалось получить ссылку на файлы
        if self.url is None:
            raise UsersParseError("Не предполагаемый элемент файлов")
        # Параметры ссылки
        parsed_url = urlparse.urlparse(self.url)
        parsed_q = urlparse.parse_qs(parsed_url.query)

        path = parsed_q.get("path")
        if path is None:
            raise UsersParseError("Не предполагаемый элемент файлов")
        # В основном ссылки не содержащие path не являются файлами
        self.file_path = path[0]
        self.file_name = os.path.basename(self.file_path.replace("\\", "/"))
        self.file_short_name = os.path.splitext(self.file_name)[0]

    def get_links(self, content_response) -> list:
        """Получение ссылок на скачивание файла"""
        links = []
        tree = html.fromstring(content_response)
        for dist in tree.find_class("downloadDist"):
            for link in dist.xpath("a"):
                links.append(link.attrib.get("href"))
        return links
