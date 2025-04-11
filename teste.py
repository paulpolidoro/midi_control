class Teste:
    def __init__(self):
        self._on_short_press = None
        self._on_long_press = True

    def in_use(self, callback):
        try:
            getattr(self, f'_{callback}')
            setattr(self, f'_{callback}', True)
            return True
        except AttributeError:
            return False

teste = Teste()

print(teste.in_use('on_short_press'))