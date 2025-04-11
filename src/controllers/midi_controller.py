import time
import mido

from typing import Callable, Optional, List
from threading import Thread

class MidiController:
    TYPE_SYSEX = 'sysex'
    TYPE_PC = 'program_change'
    TYPE_CC = 'control_change'

    def __init__(self, device_name:str):
        self._device_name = device_name

        # Controle de status
        self._wait_connect = True
        self._is_connected = False
        self._is_monitoring = False
        self._is_receiving = False

        # Threads
        self._thread_connect:Optional[Thread] = None
        self._thread_monitor:Optional[Thread] = None
        self._thread_receive:Optional[Thread] = None

        # Portas de comunicação
        self._input_port = None
        self._output_port = None
        
        # Callbacks
        self._on_connect:Optional[Callable[[],None]] = None
        self._on_disconnect:Optional[Callable[[],None]] = None
        self._on_error_connect:Optional[Callable[[Exception],None]] = None
        self._on_receive:Optional[Callable[[str, tuple],None]] = None

    def connect(self):
        if not self._is_connected:
            self._thread_connect = Thread(target=self._try_connect, daemon=True)
            self._thread_connect.start()
            
    def disconnect(self):
        if self._is_connected:
            self.stop_receive()
            self.stop_monitor()
            self._is_connected = False

        if self._input_port:
            self._input_port.close()
            
        if self._output_port:
            self._output_port.close()

        self._input_port = None
        self._output_port = None

    def start_receive(self):
        self._is_receiving = True

        if self._is_connected:
            self._thread_receive = Thread(target=self._receive_midi, daemon=True)
            self._thread_receive.start()
    
    def stop_receive(self):
        if self._is_receiving:
            self._is_receiving = False
            self._thread_receive.join()
            
    def start_monitor(self):
        self._is_monitoring = True

        if self._is_connected:
            self._thread_monitor = Thread(target=self._monitor_connection, daemon=True)
            self._thread_monitor.start()
            
    def stop_monitor(self):
        if self._is_monitoring:
            self._is_monitoring = False
            self._thread_monitor.join()

    def _try_connect(self):
        while self._wait_connect and not self._is_connected:
            print('Tentando conectar...')
            available_ports = mido.get_input_names()
            if self._device_name in available_ports:
                try:
                    self._input_port = mido.open_input(self._device_name)
                    self._output_port = mido.open_output(self._device_name)
                    
                    self._is_connected = True

                    print('Conectado com sucesso!')
                    
                    self.start_monitor()
                    self.start_receive()
                    
                    if self._on_connect:
                        self._on_connect()

                    break
                except Exception as e:
                    if self._on_error_connect:
                        self._on_error_connect(e)

            time.sleep(2)
    
    def _monitor_connection(self):
        while self._is_monitoring:
            available_ports = mido.get_input_names()
            if self._device_name not in available_ports:
                if self._on_disconnect:
                    self._on_disconnect()
                
                self._is_connected = False
                self._is_monitoring = False
                self._is_receiving = False

                self._input_port = None
                self._output_port = None

                self.connect()
                break
                
            time.sleep(2)
        
    def _receive_midi(self):
        while self._is_receiving and self._is_connected:
            for message in self._input_port.iter_pending():
                if self._on_receive:
                    self._on_receive(message.type, message.data)

    def send_pc(self, channel:int, pc:int) -> None:
        try:
            message = mido.Message(self.TYPE_PC, channel=channel, program=pc)
            self._output_port.send(message)
        except Exception as e:
            print(f"Error sending Program Change: {e}")

    def send_cc(self, channel:int, data:List[int]) -> None:
        try:
            message = mido.Message(self.TYPE_CC, channel=channel, control=data[0], value=data[1])
            self._output_port.send(message)
        except Exception as e:
            print(f"Error sending Control Change: {e}")

    def send_sysex(self, data:List[int]) -> None:
        try:
            sysex = [0xF0] + data + [0xF7]

            message = mido.Message(self.TYPE_SYSEX, data=sysex)
            self._output_port.send(message)
        except Exception as e:
            print(f"Error sending SysEx message: {e}")

    def set_on_connect(self, callback:Callable[[],None]) -> None:
        self._on_connect = callback

    def set_on_disconnect(self, callback:Callable[[],None]) -> None:
        self._on_disconnect = callback

    def set_on_error_connect(self, callback:Callable[[],None]) -> None:
        self._on_error_connect = callback

    def set_on_receive(self, callback:Callable[[str,tuple],None]) -> None:
        self._on_receive = callback