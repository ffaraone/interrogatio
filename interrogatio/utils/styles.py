class Rule:
    def __init__(self, fg='', bg='', attr=''):
        self.fg = fg
        self.bg = bg
        self.attr = attr

    def __str__(self):
        tokens = []
        if self.bg:
            tokens.append('bg:{}'.format(self.bg))
        if self.fg:
            tokens.append(self.fg)
        if self.attr:
            tokens.append(self.attr)
        return ' '.join(tokens)