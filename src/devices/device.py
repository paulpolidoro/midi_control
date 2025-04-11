from abc import ABC, abstractmethod

class Device(ABC):
    device_name: str
    brand: str
    name: str
    model: str
    max_presets:int
    presets_per_bank:int

    @abstractmethod
    def handle_midi(self, midi_type: str, data: tuple):
        pass