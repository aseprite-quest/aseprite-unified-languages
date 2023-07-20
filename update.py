import logging
import os
import shutil

from aseprite_ini import Aseini

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('format')

project_root_dir = os.path.dirname(__file__)
strings_dir = os.path.join(project_root_dir, 'assets', 'strings')
data_dir = os.path.join(project_root_dir, 'data')
alphabets_dir = os.path.join(project_root_dir, 'build', 'alphabets')


def main():
    if os.path.exists(alphabets_dir):
        shutil.rmtree(alphabets_dir)
    os.makedirs(alphabets_dir)

    logger.info("Pull 'en' strings: 'main'")
    strings_en = Aseini.pull_strings()
    for version in ['1.3-rc5', '1.2.40']:
        logger.info("Fallback 'en' strings: '%s'", version)
        strings_en.fallback(Aseini.pull_strings(f'v{version}'))
    logger.info("Update strings: 'en.ini'")
    strings_en.save(os.path.join(strings_dir, 'en.ini'))
    logger.info("Dump alphabet: 'en.txt'")
    strings_en.save_alphabet(os.path.join(alphabets_dir, 'en.txt'))

    for file_name in os.listdir(data_dir):
        if not file_name.endswith('.ini'):
            continue
        file_path = os.path.join(data_dir, file_name)
        logger.info("Update strings: '%s'", file_name)
        strings_lang = Aseini.load(file_path)
        strings_lang.save(file_path, strings_en)
        alphabet_file_name = f"{file_name.removesuffix('.ini')}.txt"
        logger.info("Dump alphabet: '%s'", alphabet_file_name)
        strings_lang.save_alphabet(os.path.join(alphabets_dir, alphabet_file_name))


if __name__ == '__main__':
    main()
