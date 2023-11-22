import os

import yaml

project_root_dir = os.path.abspath(os.path.dirname(__file__))
assets_dir = os.path.join(project_root_dir, 'assets')
strings_dir = os.path.join(assets_dir, 'strings')
data_dir = os.path.join(project_root_dir, 'data')
build_dir = os.path.join(project_root_dir, 'build')
releases_dir = os.path.join(build_dir, 'releases')
alphabets_dir = os.path.join(build_dir, 'alphabets')


class Contributor:
    @staticmethod
    def parse(configs_data: dict) -> list['Contributor']:
        return [Contributor(config_data) for config_data in configs_data]

    def __init__(self, config_data: dict):
        self.name = config_data['name']
        self.url = config_data.get('url', None)
        self.email = config_data.get('email', None)
        self.copyright_year = config_data['copyright-year']

    @property
    def copyright_line(self) -> str:
        copyright_line = f'Copyright (C) {self.copyright_year}  {self.name}'
        if self.url is not None:
            copyright_line += f' ({self.url})'
        elif self.email is not None:
            copyright_line += f' ({self.email})'
        return copyright_line


class LanguageConfig:
    @staticmethod
    def load() -> list['LanguageConfig']:
        file_path = os.path.join(os.path.dirname(__file__), 'assets', 'language-configs.yaml')
        with open(file_path, 'rb') as file:
            configs_data: dict = yaml.safe_load(file)
        return [LanguageConfig(config_data) for config_data in configs_data]

    def __init__(self, config_data: dict):
        self.id: str = config_data['id']
        self.english_name: str = config_data['english-name']
        self.display_name: str = config_data['display-name']
        self.source_repository: str = config_data['source-repository']
        self.sync_repository: str = config_data['sync-repository']
        self.sync_path: str = config_data['sync-path']
        self.contributors = Contributor.parse(config_data['contributors'])

    @property
    def file_name(self) -> str:
        return f'{self.id.lower()}.ini'

    @property
    def alphabet_file_name(self) -> str:
        return f'{self.id.lower()}.txt'

    @property
    def source_repository_url(self) -> str:
        return f'https://github.com/{self.source_repository}'

    @property
    def sync_repository_url(self) -> str:
        return f'https://github.com/{self.sync_repository}'

    @property
    def sync_url(self) -> str:
        return f'https://raw.githubusercontent.com/{self.sync_repository}/{self.sync_path}'
