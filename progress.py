import json
import logging
import os

from aseprite_ini import Aseini

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('progress')

project_root_dir = os.path.dirname(__file__)
strings_dir = os.path.join(project_root_dir, 'assets', 'strings')
data_dir = os.path.join(project_root_dir, 'data')


def main():
    package_json_file_path = os.path.join(data_dir, 'package.json')
    with open(package_json_file_path, 'r', encoding='utf-8') as file:
        languages: list[dict[str, str]] = json.loads(file.read())['contributes']['languages']

    logger.info(f"Load 'en' strings")
    strings_en = Aseini.load(os.path.join(strings_dir, 'en.ini'))

    info_lines = [
        '',
        '| English Name | Display Name | File | Translated | Missing | Progress |',
        '|---|---|---|---:|---:|---:|',
    ]
    for language in languages:
        english_name = language['englishName']
        display_name = language['displayName']
        file_name = language['path'].removeprefix('./')
        logger.info(f"Load strings: '{file_name}'")
        strings_lang = Aseini.load(os.path.join(data_dir, file_name))
        translated, total = strings_lang.coverage(strings_en)
        missing = total - translated
        progress = translated / total
        finished_emoji = '🚩' if progress == 1 else '🚧'
        info_lines.append(f'| {english_name} | {display_name} | [{file_name}](data/{file_name}) | {translated} / {total} | {missing} | {progress:.2%} {finished_emoji} |')
    info_lines.append('')

    readme_file_path = os.path.join(project_root_dir, 'README.md')
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
    logger.info(f"Update: 'README.md'")


if __name__ == '__main__':
    main()
