from collections import UserDict
from typing import Iterable


class Aseini(UserDict[str, dict[str, str]]):
    @staticmethod
    def decode(lines: Iterable[str]) -> 'Aseini':
        headers = list[str]()
        for line in lines:
            line = line.strip()
            if line == '':
                continue
            if not line.startswith('#'):
                break
            line = line.removeprefix('#').strip()
            headers.append(line)
        ini = Aseini(headers)

        section = None
        lines_iterator = iter(lines)
        line_num = 0
        for line in lines_iterator:
            line_num += 1
            line = line.strip()
            if line == '' or line.startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                section_name = line.removeprefix('[').removesuffix(']').strip()
                if section_name in ini:
                    section = ini[section_name]
                else:
                    section = dict[str, str]()
                    ini[section_name] = section
            elif '=' in line:
                assert section is not None, f'[line {line_num}]: no current section.'
                tokens = line.split('=', 1)
                key = tokens[0].strip()
                tail = tokens[1].strip()
                if tail.startswith('<<<'):
                    buffer = [tail]
                    tag = tail.removeprefix('<<<')
                    for value_line in lines_iterator:
                        line_num += 1
                        if value_line.strip() == tag:
                            break
                        buffer.append(value_line.rstrip())
                    buffer.append(tag)
                    value = '\n'.join(buffer)
                else:
                    value = tail
                if key not in section:
                    section[key] = value
            else:
                raise AssertionError(f'[line {line_num}]: token error.')
        return ini

    @staticmethod
    def load(file_path: str) -> 'Aseini':
        with open(file_path, 'r', encoding='utf-8') as file:
            return Aseini.decode(file.read().split('\n'))

    def __init__(self, headers: list[str] = None):
        super().__init__()
        if headers is None:
            headers = list[str]()
        self.headers = headers

    def fallback(self, other: 'Aseini'):
        for section_name, other_section in other.items():
            if section_name in self:
                section = self[section_name]
            else:
                section = dict[str, str]()
                self[section_name] = section
            for key, value in other_section.items():
                if key not in section:
                    section[key] = value

    def encode(self, source: 'Aseini' = None) -> list[str]:
        if source is None:
            source = self

        lines = list[str]()
        for header in self.headers:
            lines.append(f'# {header}')
        lines.append('')
        for section_name, source_section in source.items():
            lines.append(f'[{section_name}]')
            for key, source_value in source_section.items():
                value = None
                if section_name in self and key in self[section_name]:
                    value = self[section_name][key]
                if source_value.startswith('<<<'):
                    if value is None:
                        for index, value_line in enumerate(source_value.split('\n')):
                            if index == 0:
                                lines.append(f'# TODO # {key} = {value_line}')
                            else:
                                lines.append(f'# TODO # {value_line}')
                    else:
                        assert value.startswith('<<<'), f"value type incorrect: '{section_name}.{key}'"
                        for index, value_line in enumerate(value.split('\n')):
                            if index == 0:
                                lines.append(f'{key} = {value_line}')
                            else:
                                lines.append(value_line)
                else:
                    if value is None:
                        lines.append(f'# TODO # {key} = {source_value}')
                    else:
                        assert not value.startswith('<<<'), f"value type incorrect: '{section_name}.{key}'"
                        lines.append(f'{key} = {value}')
            lines.append('')
        return lines

    def save(self, file_path: str, source: 'Aseini' = None):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(self.encode(source)))
