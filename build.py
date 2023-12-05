import json
import logging
import os
import shutil
import zipfile

import configs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('build')


def _cleanup_dirs():
    if os.path.exists(configs.outputs_dir):
        shutil.rmtree(configs.outputs_dir)
    os.makedirs(configs.outputs_dir)
    logger.info(f"Cleanup dir: '{configs.outputs_dir}'")

    if os.path.exists(configs.releases_dir):
        shutil.rmtree(configs.releases_dir)
    os.makedirs(configs.releases_dir)
    logger.info(f"Cleanup dir: '{configs.releases_dir}'")


def _make_package_json_single(language_config: configs.LanguageConfig, build_version: int):
    package_data = {
        'name': f'language-{language_config.name_id}',
        'displayName': f'Language - {language_config.english_name}',
        'description': f'Aseprite Language Extension - {language_config.english_name}',
        'version': f'{configs.aseprite_version}-build-{build_version}',
        'author': {
            'name': 'Aseprite Quest',
            'url': 'https://github.com/aseprite-quest',
        },
        'contributors': [],
        'publisher': 'Aseprite Quest',
        'license': 'CC-BY-4.0',
        'categories': [
            'Languages',
        ],
        'contributes': {
            'languages': [{
                'id': language_config.id,
                'path': f'./{language_config.file_name}',
                'englishName': language_config.english_name,
                'displayName': language_config.display_name,
            }],
        }
    }

    for contributor in language_config.contributors:
        contributor_data = {
            'name': contributor.name,
        }
        if contributor.url is not None:
            contributor_data['url'] = contributor.url
        if contributor.email is not None:
            contributor_data['email'] = contributor.email
        package_data['contributors'].append(contributor_data)

    file_path = os.path.join(configs.outputs_dir, f'package-{language_config.id.lower()}.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(package_data, indent=2, ensure_ascii=False))
        file.write('\n')
    logger.info(f"Make package json: '{file_path}'")


def _make_package_json_merged(language_configs: list[configs.LanguageConfig], build_version: int):
    package_data = {
        'name': 'language-all',
        'displayName': 'Language - All',
        'description': 'Aseprite Language Extension - All',
        'version': f'{configs.aseprite_version}-build-{build_version}',
        'author': {
            'name': 'Aseprite Quest',
            'url': 'https://github.com/aseprite-quest',
        },
        'contributors': [],
        'publisher': 'Aseprite Quest',
        'license': 'CC-BY-4.0',
        'categories': [
            'Languages',
        ],
        'contributes': {
            'languages': [],
        }
    }

    name_to_contributor_data = {}
    for language_config in language_configs:
        for contributor in language_config.contributors:
            if contributor.name in name_to_contributor_data:
                contributor_data = name_to_contributor_data[contributor.name]
            else:
                contributor_data = {
                    'name': contributor.name,
                }
                name_to_contributor_data[contributor.name] = contributor_data
            if contributor.url is not None:
                contributor_data['url'] = contributor.url
            if contributor.email is not None:
                contributor_data['email'] = contributor.email

        package_data['contributes']['languages'].append({
            'id': language_config.id,
            'path': f'./{language_config.file_name}',
            'englishName': language_config.english_name,
            'displayName': language_config.display_name,
        })
    package_data['contributors'].extend(name_to_contributor_data.values())

    file_path = os.path.join(configs.outputs_dir, 'package-all.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(package_data, indent=2, ensure_ascii=False))
        file.write('\n')
    logger.info(f"Make package json: '{file_path}'")


def _make_extension_single(language_config: configs.LanguageConfig, build_version: int):
    file_path = os.path.join(configs.releases_dir, f'language-{language_config.name_id}-v{configs.aseprite_version}-build-{build_version}.aseprite-extension')
    with zipfile.ZipFile(file_path, 'w') as file:
        file.write(os.path.join(configs.outputs_dir, f'package-{language_config.id.lower()}.json'), 'package.json')
        file.write(os.path.join(configs.data_dir, language_config.file_name), language_config.file_name)
    logger.info(f"Make extension: '{file_path}'")
        

def _make_extension_merged(language_configs: list[configs.LanguageConfig], build_version: int):
    file_path = os.path.join(configs.releases_dir, f'language-all-v{configs.aseprite_version}-build-{build_version}.aseprite-extension')
    with zipfile.ZipFile(file_path, 'w') as file:
        file.write(os.path.join(configs.outputs_dir, 'package-all.json'), 'package.json')
        for language_config in language_configs:
            file.write(os.path.join(configs.data_dir, language_config.file_name), language_config.file_name)
    logger.info(f"Make extension: '{file_path}'")


def main():
    _cleanup_dirs()
    language_configs = configs.LanguageConfig.load()
    for language_config in language_configs:
        _make_package_json_single(language_config, 1)
        _make_extension_single(language_config, 1)
    _make_package_json_merged(language_configs, 1)
    _make_extension_merged(language_configs, 1)


if __name__ == '__main__':
    main()
