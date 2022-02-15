class Board():
    def __init__(self, id: str, last_modified: int) -> None:
        self.id = id
        self.last_modified = last_modified


class Thread():
    def __init__(self, board: Board, id: int, last_updated: int) -> None:
        self.board = board
        self.id = id
        self.last_updated = last_updated


class File():
    def __init__(self, id: int, filename: str, ext: str, fsize: int) -> None:
        self.id = id
        self.filename = filename
        self.ext = ext
        self.fsize = fsize


class Post():
    def __init__(self, thread: Thread, id: int, file: File) -> None:
        self.thread = thread
        self.id = id
        self.file = file


class Settings():
    def __init__(self, boards: list[str], use_keywords: bool = False, keywords: list[str] = [], use_ignored_words: bool = False, ignored_words: list[str] = [], images_only: bool = False, board_refresh_time: int = 60, min_replies: int = 10):
        self.BOARDS = boards
        self.USE_KEYWORDS = use_keywords
        self.KEYWORDS = keywords
        self.USE_IGNORED_WORDS = use_ignored_words
        self.IGNORED_WORDS = ignored_words
        self.IMAGES_ONLY = images_only
        self.MINIMAL_BOARD_REFRESH_TIME = board_refresh_time
        self.MIN_REPLIES = min_replies
