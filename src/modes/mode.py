from abc import ABC, abstractmethod
from typing import List

from src.components.display import Display
from src.components.foot import Foot
from src.components.multi_foot import MultiFoot


class Mode:
    def __init__(self, display: Display, foots:List[Foot], multi_foots:MultiFoot):
        self._display = display
        self._foots = foots
        self._multi_foots = multi_foots

        self._display.set_default_view(self._default_view)

    @abstractmethod
    def _default_view(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

