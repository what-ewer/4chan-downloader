from configparser import ConfigParser

from src.model import Settings


class SettingsParser:

    def __init__(self) -> None:
        self.config = ConfigParser()

    def get_config(self, config_file: str) -> Settings:
        self.config.read(config_file)
        settings = Settings(
            boards=self.config.get('FILTERS', 'Boards').split(','),
            use_keywords=self.config['FILTERS'].getboolean('UseKeywords'),
            keywords=self.config['FILTERS'].get('Keywords').split(','),
            use_ignored_words=self.config['FILTERS'].getboolean(
                'UseIgnoredWords'),
            ignored_words=self.config['FILTERS'].get(
                'IgnoredWords').split(','),
            images_only=self.config['SETTINGS'].getboolean('ImagesOnly'),
            board_refresh_time=self.config['SETTINGS'].getint(
                'MinimalBoardRefreshTime'),
            min_replies=self.config['SETTINGS'].getint('MinimumReplies')
        )
        return settings
