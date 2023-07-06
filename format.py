import logging
import os

from utils.aseini import Aseini

project_root_dir = os.path.dirname(__file__)
strings_dir = os.path.join(project_root_dir, 'assets', 'strings')
data_dir = os.path.join(project_root_dir, 'data')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('format')


def main():
    logger.info(f"Load 'en' strings: 'main'")
    en_stings = Aseini.load(os.path.join(strings_dir, 'main', 'en.ini'))
    for version in ['1.3-rc4', '1.2.40']:
        logger.info(f"Fallback 'en' strings: '{version}'")
        en_stings.fallback(Aseini.load(os.path.join(strings_dir, version, 'en.ini')))
    logger.info(f"Mix 'en' strings")
    en_stings.save(os.path.join(strings_dir, 'en.ini'))

    for file_name in os.listdir(data_dir):
        if not file_name.endswith('.ini'):
            continue
        file_path = os.path.join(data_dir, file_name)
        logger.info(f"Format strings: '{file_name}'")
        lang_strings = Aseini.load(file_path)
        lang_strings.save(file_path, en_stings)


if __name__ == '__main__':
    main()
