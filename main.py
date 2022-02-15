from queue import Queue
from time import sleep, time
from requests import Response

from src.model import Board, Thread, Post, File, Settings
from src.logger import Logger
from src.web_requests import WebRequests
from src.utils import FileManager, InterestChecker
from src.parser import SettingsParser


class RequestManager:

    def __init__(self, settings: Settings) -> None:
        self.boards = [Board(b, 0) for b in settings.BOARDS]
        self.threads = Queue()
        self.posts = Queue()

        self.settings = settings

        self.file_manager = FileManager()
        self.interest_checker = InterestChecker(settings)
        self.logger = Logger()
        self.requests = WebRequests()

        self.__main_loop()

    def __main_loop(self):
        while True:
            for b in self.boards:
                minimum_time = b.last_modified + self.settings.MINIMAL_BOARD_REFRESH_TIME
                curr_time = time()
                if minimum_time > curr_time:
                    sleep(minimum_time - curr_time)

                self.__get_resource(self.__get_threads, b)

            while not self.threads.empty():
                thread: Thread = self.threads.get()
                self.__get_resource(self.__get_posts, thread)
                self.threads.task_done()

            while not self.posts.empty():
                post: Post = self.posts.get()
                self.__get_resource(self.__get_file, post)
                self.posts.task_done()

    def __get_resource(self, f, resource) -> None:
        try:
            f(resource)
            self.logger.successfully_got_resource(resource)
        except Exception:
            self.logger.failed_to_get_resource(resource)
        finally:
            sleep(1.5)

    def __get_threads(self, b: Board) -> None:
        additional_info = self.settings.USE_IGNORED_WORDS or self.settings.USE_KEYWORDS
        res: Response = self.requests.request_resource(b, additional_info)
        match res.status_code:
            case 200:
                pass
            case 304:
                self.logger.requested_resource_not_modified(b)
                return
            case _:
                raise Exception(res.status_code)

        res_json = res.json()
        request_time = time()

        for p in res_json:
            threads = p['threads']
            for t in threads:
                if t['last_modified'] > b.last_modified:
                    new_t = Thread(b, t['no'], b.last_modified)
                    if self.interest_checker.check_interest(t):
                        self.threads.put(new_t)
                else:
                    break
            else:
                continue
            break

        b.last_modified = int(request_time)

    def __get_posts(self, t: Thread) -> None:
        res: Response = self.requests.request_resource(t)
        match res.status_code:
            case 200:
                pass
            case 304:
                self.logger.requested_resource_not_modified(t)
                return
            case _:
                raise Exception(res.status_code)

        res_json = res.json()

        if not self.settings.IMAGES_ONLY:
            self.file_manager.download_thread(t, res)

        posts = res_json['posts']
        posts.reverse()

        for p in posts:
            if p['time'] > t.last_updated:
                if 'tim' in p.keys():
                    new_p = Post(t, p['no'], File(
                        p['tim'], p['filename'], p['ext'], p['fsize']))
                    self.posts.put(new_p)
            else:
                break

    def __get_file(self, p: Post) -> None:
        res: Response = self.requests.request_resource(p)
        match res.status_code:
            case 200:
                pass
            case 304:
                self.logger.requested_resource_not_modified(p)
                return
            case _:
                raise Exception(res.status_code)

        self.file_manager.download_file(p, res)


if __name__ == "__main__":
    parser = SettingsParser()
    settings = parser.get_config('config.ini')
    request_manager = RequestManager(settings)
