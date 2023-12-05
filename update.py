import hashlib
import json
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

    versions_file_path = os.path.join(configs.assets_dir, 'language-versions.json')
    with open(versions_file_path, 'r', encoding='utf-8') as file:
        versions_data: dict = json.loads(file.read())
    any_version_changed = False

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

        sha256 = hashlib.sha256()
        sha256.update(strings_lang.encode_str(strings_en).encode('utf-8'))
        sha256_hex = sha256.hexdigest()
        if language_config.id in versions_data:
            version_data = versions_data[language_config.id]
            if version_data['sha256'] != sha256_hex:
                version_data['build'] += 1
                version_data['sha256'] = sha256_hex
                any_version_changed = True
        else:
            versions_data[language_config.id] = {
                'build': 1,
                'sha256': sha256_hex,
            }
            any_version_changed = True

        translated, total = strings_lang.coverage(strings_en)
        missing = total - translated
        progress = translated / total
        finished_emoji = '🚩' if progress == 1 else '🚧'
        info_lines.append(f'| {language_config.english_name} | [{language_config.source_repository}]({language_config.source_repository_url}) | {translated} / {total} | {missing} | {progress:.2%} {finished_emoji} |')

    if any_version_changed:
        versions_data['all']['build'] += 1

    with open(versions_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(versions_data, indent=2, ensure_ascii=False))
        file.write('\n')
    logger.info("Update: '%s'", versions_file_path)

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
    logger.info("Update: '%s'", readme_file_path)


if __name__ == '__main__':
    main()
