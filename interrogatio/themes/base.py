from prompt_toolkit.styles import Style, default_ui_style, merge_styles


_interrogatio_default = Style([
    ('interrogatio.question', '#efa147'),
    ('interrogatio.error', '#ff0000'),
    ('', 'ansiblue'),
    ('label', '#efa147'),
    ('radio', '#efa147'),
    ('radio-checked', 'ansiblue'),
    ('radio-selected', 'ansigreen'),
    ('dialog.body text-area', 'bg:default #0000ff'),
    ('dialog.body text-area last-line', 'underline')
])



_default_theme = merge_styles([
    default_ui_style(),
    _interrogatio_default
])

_current_theme = _default_theme

def get_default_theme():
    return _default_theme

def get_current_theme():
    return _current_theme

def set_current_theme(theme):
    _current_theme = theme
