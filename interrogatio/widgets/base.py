from prompt_toolkit.widgets import RadioList as BaseRadioList
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.application.current import get_app


class RadioList(BaseRadioList):
    def __init__(self, values=[], default=None, accept_handler=None, **kwargs):
        super(RadioList, self).__init__(values)
        self.accept_handler = accept_handler
        for i in range(len(self.values)):
            if self.values[i][0] == default:
                self._selected_index = i
                self.current_value = self.values[i][0]
                break
        
        self.window.right_margins = []

        kb = KeyBindings()

        @kb.add('enter')
        @kb.add(' ')
        def _(event):
            self.current_value = self.values[self._selected_index][0]
            if self.accept_handler:
                self.accept_handler(self.current_value)
        
        self.control.key_bindings = merge_key_bindings([
            self.control.get_key_bindings(), kb])