import json
import logging
import os

import configs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('info')


def _build_contributors_info(language_configs: list[configs.LanguageConfig]) -> list[dict]:
    contributors_info = {}
    for language_config in language_configs:
        for contributor in language_config.contributors:
            if contributor.name in contributors_info:
                contributor_info = contributors_info[contributor.name]
            else:
                contributor_info = {}
                contributors_info[contributor.name] = contributor_info
            contributor_info['name'] = contributor.name
            if contributor.url is not None:
                contributor_info['url'] = contributor.url
            if contributor.email is not None:
                contributor_info['email'] = contributor.email
    return [contributor_info for contributor_info in contributors_info.values()]


def _build_languages_info(language_configs: list[configs.LanguageConfig]) -> list[dict]:
    languages_info = []
    for language_config in language_configs:
        language_info = {
            'id': language_config.id,
            'path': f'./{language_config.file_name}',
            'englishName': language_config.english_name,
            'displayName': language_config.display_name,
        }
        languages_info.append(language_info)
    return languages_info


def main():
    language_configs = configs.LanguageConfig.load()

    package_json_file_path = os.path.join(configs.data_dir, 'package.json')
    with open(package_json_file_path, 'r', encoding='utf-8') as file:
        package_info: dict = json.loads(file.read())

    package_info['contributors'] = _build_contributors_info(language_configs)
    package_info['contributes']['languages'] = _build_languages_info(language_configs)

    with open(package_json_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(package_info, indent=2, ensure_ascii=False))
        file.write('\n')
    logger.info("Update: 'package.json'")


if __name__ == '__main__':
    main()
