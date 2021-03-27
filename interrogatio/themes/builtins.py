import os

from interrogatio.themes.base import register, Theme


class DefaultTheme(Theme):
    def __init__(self):
        super(DefaultTheme, self).__init__()
        self.load(os.path.join(
            os.path.dirname(__file__),
            'theme_files',
            'default.json',
        ))


register('default', DefaultTheme())


class PurpleTheme(Theme):
    def __init__(self):
        super(PurpleTheme, self).__init__()
        self.load(os.path.join(
            os.path.dirname(__file__),
            'theme_files',
            'purple.json',
        ))


register('purple', PurpleTheme())
