# Aseprite Unified Languages Extension

[![Releases](https://img.shields.io/github/v/release/aseprite-quest/aseprite-unified-languages-extension)](https://github.com/aseprite-quest/aseprite-unified-languages-extension/releases)

[Aseprite](https://github.com/aseprite/aseprite) extension to support multiple languages.

![product](docs/product.png)

## Supported languages

| English Name | Display Name | File | Translated | Missing | Progress |
|---|---|---|---:|---:|---:|
| Chinese (Simplified) | 中文（简体） | [zh-hans.ini](data/zh-hans.ini) | 1587 / 1587 | 0 | 100.00% 🚩 |
| Chinese (Traditional) | 中文（繁體） | [zh-hant.ini](data/zh-hant.ini) | 922 / 1587 | 665 | 58.10% 🚧 |
| Japanese | 日本語 | [ja.ini](data/ja.ini) | 1199 / 1587 | 388 | 75.55% 🚧 |
| Korean | 한국어 | [ko.ini](data/ko.ini) | 1199 / 1587 | 388 | 75.55% 🚧 |
| Russian | Русский | [ru.ini](data/ru.ini) | 1578 / 1587 | 9 | 99.43% 🚧 |
| Italian | Italiano | [it.ini](data/it.ini) | 1587 / 1587 | 0 | 100.00% 🚩 |

## Usage

Download the latest version `.aseprite-extension` file in the [Releases](https://github.com/aseprite-quest/aseprite-unified-languages-extension/releases), and then follow the [Documentation](https://www.aseprite.org/docs/extensions/) to install it.

## How to contribute

This extension follows the [Aseprite Language Extension Specification](https://www.aseprite.org/docs/extensions/languages/).

All the localized files are in the [data](data) directory, named with [IETF language tag](https://en.wikipedia.org/wiki/IETF_language_tag) `.ini`.

The contents are corresponding with the default language English [`assets/strings/en.ini`](assets/strings/en.ini).

Translate these files and [pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) to this repository.

## Dependencies

- [Aseprite INI](https://github.com/aseprite-quest/aseprite-ini)

## References

- [Aseprite Docs - Extensions - Languages](https://aseprite.org/docs/extensions/languages)
- [IETF language tag](https://en.wikipedia.org/wiki/IETF_language_tag)
- [Letter codes of cultures (languages, countries / regions) - list](https://www.venea.net/web/culture_code)
- [MDN - CSS pseudo-class - :lang()](https://developer.mozilla.org/en-US/docs/Web/CSS/:lang)
- [Simplified Chinese](https://github.com/J-11/Aseprite-Simplified-Chinese)
- [Traditional Chinese](https://github.com/chongx1an/Aseprite-TraditionalChineseExtension)
- [Japanese](https://wikiwiki.jp/aseprite/日本語化ファイルのダウンロード)
- [Korean](https://github.com/ImBada/Aseprite-Korean)
- [Russian](https://github.com/lufog/aseprite-language-russian)
- [Italian](https://github.com/FabianoIlCapo/aseprite_italian)

## License

Translations are under the [Creative Commons Attribution 4.0 International License](data/LICENSE.txt).

Scripts are under the [MIT License](LICENSE).
