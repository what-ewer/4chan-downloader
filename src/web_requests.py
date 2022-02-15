from requests import Session, Response
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

from src.model import Board, Thread, Post


class WebRequests:
    def __init__(self) -> None:
        self.retry_strategy = Retry(total=3,
                                    backoff_factor=2.5,
                                    status_forcelist=[500, 502, 503, 504])
        self.adapter = HTTPAdapter(max_retries=self.retry_strategy)
        self.http = Session()
        self.http.mount("https://", self.adapter)
        self.headers = {"If-Modified-Since": None}

    def request_resource(self, requested: object, additional_info: bool = False) -> Response:
        self.__update_headers(requested)
        link = self.__get_request_link(requested, additional_info)
        match requested:
            case Post():
                response = self.http.get(
                    link, headers=self.headers, stream=True)
            case _:
                response = self.http.get(link, headers=self.headers)
        return response

    def __get_request_link(self, requested: object, additional_info: bool = False) -> str:
        match requested:
            case Board():
                if additional_info:
                    return f"https://a.4cdn.org/{requested.id}/catalog.json"
                else:
                    return f"https://a.4cdn.org/{requested.id}/threads.json"
            case Thread():
                return f"https://a.4cdn.org/{requested.board.id}/thread/{requested.id}.json"
            case Post():
                return f"https://i.4cdn.org/{requested.thread.board.id}/{requested.file.id}{requested.file.ext}"
            case _:
                raise TypeError("Wrong requested resource")

    def __update_headers(self, requested: object) -> None:
        # If-Modified-Since: <day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT
        modified_last = 0
        match requested:
            case Board():
                modified_last = requested.last_modified
            case Thread():
                modified_last = requested.last_updated
            case Post():
                modified_last = requested.thread.last_updated

        self.headers["If-Modified-Since"] = self.__get_date_from_timestamp(
            modified_last)

    def __get_date_from_timestamp(self, timestamp: int) -> str:
        return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(timestamp))
