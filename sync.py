import logging
import os

from aseprite_ini import Aseini

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sync')

project_root_dir = os.path.dirname(__file__)
strings_dir = os.path.join(project_root_dir, 'assets', 'strings')
data_dir = os.path.join(project_root_dir, 'data')

sync_configs = {
    'zh-hans.ini': 'https://raw.githubusercontent.com/aseprite-quest/aseprite-language-chinese-simplified/master/data/zh-hans.ini',
    'ru.ini': 'https://raw.githubusercontent.com/lufog/aseprite-language-russian/main/russian-language/ru.ini',
    'it.ini': 'https://raw.githubusercontent.com/FabianoIlCapo/aseprite_italian/master/data/it.ini',
}


def main():
    strings_en = Aseini.load(os.path.join(strings_dir, 'en.ini'))
    logger.info("Load strings: 'en.ini'")

    for file_name, url in sync_configs.items():
        file_path = os.path.join(data_dir, file_name)
        strings_lang = Aseini.load(file_path)
        strings_lang.patch(Aseini.pull_strings_by_url(url))
        strings_lang.save(file_path, strings_en)
        logger.info("Sync strings: '%s'", file_name)


if __name__ == '__main__':
    main()
