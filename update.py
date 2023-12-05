import logging
import os

from aseprite_ini import Aseini

import configs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('update')


def main():
    strings_en = Aseini.pull_strings(f'v{configs.aseprite_version}')
    strings_en.save(os.path.join(configs.strings_dir, 'en.ini'))
    logger.info("Update strings: 'en.ini'")

    info_lines = [
        '| Language | Repository | Translated | Missing | Progress |',
        '|---|---|---:|---:|---:|',
    ]

    language_configs = configs.LanguageConfig.load()
    for language_config in language_configs:
        file_path = os.path.join(configs.data_dir, language_config.file_name)
        strings_lang = Aseini.pull_strings_by_url(language_config.sync_url)
        strings_lang.headers = language_config.create_ini_headers()
        strings_lang.save(file_path, strings_en)
        logger.info("Update strings: '%s'", language_config.file_name)

        translated, total = strings_lang.coverage(strings_en)
        missing = total - translated
        progress = translated / total
        finished_emoji = '🚩' if progress == 1 else '🚧'
        info_lines.append(f'| {language_config.english_name} | [{language_config.source_repository}]({language_config.source_repository_url}) | {translated} / {total} | {missing} | {progress:.2%} {finished_emoji} |')

    readme_file_path = os.path.join(configs.project_root_dir, 'README.md')
    front_lines = []
    behind_lines = []
    with open(readme_file_path, 'r', encoding='utf-8') as file:
        current_lines = front_lines
        for line in file.readlines():
            line = line.rstrip()
            if line == '## Supported languages':
                current_lines.append(line)
                current_lines.append('')
                current_lines = None
            elif current_lines is None and line.startswith('## '):
                current_lines = behind_lines
                current_lines.append('')
                current_lines.append(line)
            elif current_lines is not None:
                current_lines.append(line)
    with open(readme_file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(front_lines + info_lines + behind_lines))
        file.write('\n')
    logger.info("Update: 'README.md'")


if __name__ == '__main__':
    main()
