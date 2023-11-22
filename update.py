import logging
import os

from aseprite_ini import Aseini

import configs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('update')


def main():
    strings_en = Aseini.pull_strings('v1.3-rc8')
    strings_en.save(os.path.join(configs.strings_dir, 'en.ini'))
    logger.info("Update strings: 'en.ini'")

    language_configs = configs.LanguageConfig.load()
    for language_config in language_configs:
        file_path = os.path.join(configs.data_dir, language_config.file_name)
        strings_lang = Aseini.load(file_path)
        strings_lang.save(file_path, strings_en)
        logger.info("Update strings: '%s'", language_config.file_name)


if __name__ == '__main__':
    main()
