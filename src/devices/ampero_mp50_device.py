from typing import Optional, Callable
from src.devices.ampero_mp100_device import AmperoMP100Device


class AmperoMP50Device(AmperoMP100Device):
    name = "Ampero MP50"
    model = "MP50"
    device_name = "HOTONE MP50 PRODUCT:HOTONE MP50 PRODUCT MIDI 1 20:0"

    def __init__(self, on_get_tap:Optional[Callable[[int], None]]=None, on_get_preset_change:Optional[Callable[[int], None]]=None):
        super().__init__(on_get_tap, on_get_preset_change)