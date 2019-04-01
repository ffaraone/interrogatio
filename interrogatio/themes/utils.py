def to_style_token(fg='', bg='', attr=''):
    tokens = []
    if bg:
        tokens.append('bg:{}'.format(bg))
    if fg:
        tokens.append(fg)
    if attr:
        tokens.append(attr)
    return ' '.join(tokens)
