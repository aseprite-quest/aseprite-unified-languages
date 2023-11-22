import logging
import os

from aseprite_ini import Aseini

import configs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('progress')


def main():
    strings_en = Aseini.load(os.path.join(configs.strings_dir, 'en.ini'))
    logger.info("Load strings: 'en.ini'")

    info_lines = [
        '',
        '| English Name | Display Name | Source | Sync | Translated | Missing | Progress |',
        '|---|---|---|---|---:|---:|---:|',
    ]
    language_configs = configs.LanguageConfig.load()
    for language_config in language_configs:
        strings_lang = Aseini.load(os.path.join(configs.data_dir, language_config.file_name))
        logger.info("Load strings: '%s'", language_config.file_name)
        translated, total = strings_lang.coverage(strings_en)
        missing = total - translated
        progress = translated / total
        finished_emoji = '🚩' if progress == 1 else '🚧'
        info_lines.append(f'| {language_config.english_name} | {language_config.display_name} | [Link]({language_config.source_repository_url}) | [Link]({language_config.sync_repository_url}) | {translated} / {total} | {missing} | {progress:.2%} {finished_emoji} |')
    info_lines.append('')

    readme_file_path = os.path.join(configs.project_root_dir, 'README.md')
    front_lines = []
    back_lines = []
    with open(readme_file_path, 'r', encoding='utf-8') as file:
        current_lines = front_lines
        for line in file.readlines():
            line = line.rstrip()
            if line == '## Supported languages':
                current_lines.append(line)
                current_lines = None
            elif current_lines is None and line.startswith('## '):
                current_lines = back_lines
                current_lines.append(line)
            elif current_lines is not None:
                current_lines.append(line)
    with open(readme_file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(front_lines + info_lines + back_lines))
        file.write('\n')
    logger.info("Update: 'README.md'")


if __name__ == '__main__':
    main()
