import logging
import os
import shutil

from aseprite_ini import Aseini

import configs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('update')


def main():
    if os.path.exists(configs.alphabets_dir):
        shutil.rmtree(configs.alphabets_dir)
    os.makedirs(configs.alphabets_dir)

    strings_en = Aseini.pull_strings('v1.3-rc8')
    strings_en.save(os.path.join(configs.strings_dir, 'en.ini'))
    logger.info("Update strings: 'en.ini'")

    strings_en.save_alphabet(os.path.join(configs.alphabets_dir, 'en.txt'))
    logger.info("Dump alphabet: 'en.txt'")

    language_configs = configs.LanguageConfig.load()
    for language_config in language_configs:
        file_path = os.path.join(configs.data_dir, language_config.file_name)
        strings_lang = Aseini.load(file_path)
        strings_lang.save(file_path, strings_en)
        logger.info("Update strings: '%s'", language_config.file_name)

        strings_lang.save_alphabet(os.path.join(configs.alphabets_dir, language_config.alphabet_file_name))
        logger.info("Dump alphabet: '%s'", language_config.alphabet_file_name)


if __name__ == '__main__':
    main()
