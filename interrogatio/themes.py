from prompt_toolkit.styles import Style, default_ui_style, merge_styles


_interrogatio_default = Style([
    ('interrogatio.question', '#efa147'),
    ('', 'ansiblue'),
])
    

_default_theme = merge_styles([
    default_ui_style(),
    _interrogatio_default
])

def get_default_theme():
    return _default_theme
