import os

from utils.aseini import Aseini

project_root_dir = os.path.dirname(__file__)
strings_dir = os.path.join(project_root_dir, 'assets', 'strings')
data_dir = os.path.join(project_root_dir, 'data')


def main():
    en_stings = Aseini.load(os.path.join(strings_dir, 'main', 'en.ini'))
    en_stings.fallback(Aseini.load(os.path.join(strings_dir, '1.3-rc4', 'en.ini')))
    en_stings.fallback(Aseini.load(os.path.join(strings_dir, '1.2.40', 'en.ini')))


if __name__ == '__main__':
    main()
