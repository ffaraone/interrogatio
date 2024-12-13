import os

from interrogatio.themes.base import Theme, register


class DefaultTheme(Theme):
    def __init__(self):
        super().__init__()
        self.load(
            os.path.join(
                os.path.dirname(__file__),
                "theme_files",
                "default.json",
            )
        )


register("default", DefaultTheme())


class PurpleTheme(Theme):
    def __init__(self):
        super().__init__()
        self.load(
            os.path.join(
                os.path.dirname(__file__),
                "theme_files",
                "purple.json",
            )
        )


register("purple", PurpleTheme())
