from os import makedirs
from os.path import exists
from simplejson import dumps, loads
from requests import Response

from src.model import Settings, Thread, Post


class FileManager:

    def __init__(self) -> None:
        self.__create_folders_if_not_exists("./downloads")

    def download_file(self, p: Post, res: Response) -> None:
        dir = self.__get_dir_name(p)
        file = self.__get_file_name(p)

        with open(dir+file, 'wb') as f:
            for chunk in res.iter_content():
                f.write(chunk)

    def download_thread(self, t: Thread, res: Response) -> None:
        thread_path = f"./downloads/{t.board.id}/{t.id}/"
        self.__create_folders_if_not_exists(thread_path)

        with open(thread_path + "thread.json", 'w') as thread_file:
            thread_file.write(
                dumps(loads(res.content), indent=4, sort_keys=True))

    @staticmethod
    def get_file_size(fsize: int, suffix="B") -> str:
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(fsize) < 1024.0:
                return f"{fsize:3.1f}{unit}{suffix}"
            fsize /= 1024.0
        return f"{fsize:.1f}Yi{suffix}"

    def __create_folders_if_not_exists(self, dir) -> None:
        if not exists(dir):
            makedirs(dir)

    def __get_dir_name(self, p: Post) -> str:
        return f"./downloads/{p.thread.board.id}/{p.thread.id}/"

    def __get_file_name(self, p: Post) -> str:
        return f"{p.file.id}{p.file.ext}"


class InterestChecker:
    def __init__(self, settings: Settings) -> None:
        self.min_replies = settings.MIN_REPLIES
        self.use_keywords = settings.USE_KEYWORDS
        self.use_ignored = settings.USE_IGNORED_WORDS
        self.keywords = settings.KEYWORDS
        self.ignored_words = settings.IGNORED_WORDS

    def check_interest(self, t) -> bool:
        if t['replies'] < self.min_replies:
            return False

        if self.use_ignored and not self.__check_ignored(t):
            return False

        if self.use_keywords and not self.__check_keywords(t):
            return False

        return True

    def __check_ignored(self, t) -> bool:
        return not self.__word_in_thread(self.ignored_words, t)

    def __check_keywords(self, t) -> bool:
        return self.__word_in_thread(self.keywords, t)

    def __word_in_thread(self, words: list[str], t):
        sub = t['sub'].lower() if 'sub' in t.keys() else ""
        com = t['com'].lower() if 'com' in t.keys() else ""
        for w in words:
            if w in sub or w in com:
                return True
        return False
