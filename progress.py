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

    strings_en = Aseini.load(os.path.join(strings_dir, 'en.ini'))
    logger.info("Load strings: 'en.ini'")

    info_lines = [
        '',
        '| English Name | Display Name | Source | Mirror | Translated | Missing | Progress |',
        '|---|---|---|---|---:|---:|---:|',
    ]
    for language in languages:
        english_name = language['englishName']
        display_name = language['displayName']
        file_name = language['path'].removeprefix('./')
        source_repository = language['sourceRepository']
        source_repository_url = f'https://github.com/{source_repository}'
        mirror_repository = language['mirrorRepository']
        mirror_repository_url = f'https://github.com/{mirror_repository}'
        strings_lang = Aseini.load(os.path.join(data_dir, file_name))
        logger.info("Load strings: '%s'", file_name)
        translated, total = strings_lang.coverage(strings_en)
        missing = total - translated
        progress = translated / total
        finished_emoji = '🚩' if progress == 1 else '🚧'
        info_lines.append(f'| {english_name} | {display_name} | [Link]({source_repository_url}) | [Link]({mirror_repository_url}) | {translated} / {total} | {missing} | {progress:.2%} {finished_emoji} |')
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
    logger.info("Update: 'README.md'")


if __name__ == '__main__':
    main()
