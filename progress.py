import logging
import os

from utils.aseini import Aseini

lang_names = {
    'zh-chs.ini': 'Simplified Chinese',
    'zh-cht.ini': 'Traditional Chinese',
    'ja.ini': 'Japanese',
}

project_root_dir = os.path.dirname(__file__)
strings_dir = os.path.join(project_root_dir, 'assets', 'strings')
data_dir = os.path.join(project_root_dir, 'data')

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('progress')


def main():
    logger.info(f"Load 'en' strings")
    en_stings = Aseini.load(os.path.join(strings_dir, 'en.ini'))

    infos = {}
    for file_name in os.listdir(data_dir):
        if not file_name.endswith('.ini'):
            continue
        logger.info(f"Load strings: '{file_name}'")
        lang_strings = Aseini.load(os.path.join(data_dir, file_name))
        total = 0
        count = 0
        for section_name, section in en_stings.items():
            for key in section:
                total += 1
                if section_name in lang_strings and key in lang_strings[section_name]:
                    count += 1
        infos[file_name] = count, total

    info_lines = [
        '',
        '| Name | File | Count | Missing | Progress |',
        '|---|---|---:|---:|---:|',
    ]
    for file_name, lang_name in lang_names.items():
        count, total = infos[file_name]
        missing = total - count
        progress = count / total
        finished_emoji = '🚩' if progress == 1 else '🚧'
        info_lines.append(f'| {lang_name} | [{file_name}](data/{file_name}) | {count} / {total} | {missing} | {progress:.2%} {finished_emoji} |')
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
