import time
import mido
import threading
#from src.devices.ampero_mp80 import AmperoMP80


class MidiController:
    TYPE_SYSEX = 'sysex'
    TYPE_PC = 'program_change'
    TYPE_CC = 'cc'

    def __init__(self, input_name, output_name, receive_callback):
        """
        Initializes the MidiController class.

        :param input_name: Name of the MIDI input port.
        :param output_name: Name of the MIDI output port.
        :param receive_callback: Callback function to handle received MIDI messages.
        """
        self.input_name = input_name
        self.output_name = output_name
        self.receive_callback = receive_callback
        self.running = False
        self.thread = None

        self.input_port = None
        self.output_port = None

    def connect_ports(self):
        """
        Attempts to connect to the MIDI input and output ports.
        """
        while True:
            available_ports = mido.get_input_names()
            if self.input_name in available_ports:
                try:
                    self.input_port = mido.open_input(self.input_name)
                    self.output_port = mido.open_output(self.output_name)
                    print(f"Connected to MIDI ports: {self.input_name}, {self.output_name}")
                    break
                except Exception as e:
                    print(f"Error connecting to MIDI ports: {e}")
            else:
                print(f"Waiting for device {self.input_name} to connect...")
            time.sleep(2)

    def _receive_midi_loop(self):
        """
        Loop to receive MIDI messages, executed in a thread.
        """
        while self.running:
            for message in self.input_port.iter_pending():
                self.receive_callback(message.data)

    def start_receiving(self):
        """
        Starts the loop to receive MIDI messages in a separate thread.
        """
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._receive_midi_loop, daemon=True)
            self.thread.start()
            print("MIDI receiving thread started.")

    def stop_receiving(self):
        """
        Stops the loop for receiving MIDI messages.
        """
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
            print("MIDI receiving thread stopped.")

    def send_pc(self, channel, pc):
        """
        Sends a Program Change (PC) message to the output.

        :param channel: MIDI channel (0-15).
        :param pc: Program change number (0-127).
        """
        try:
            message = mido.Message('program_change', channel=channel, program=pc)
            self.output_port.send(message)
            print(f"Program Change sent - Channel: {channel}, Program: {pc}")
        except Exception as e:
            print(f"Error sending Program Change: {e}")

    def send_cc(self, channel, data1, data2):
        """
        Sends a Control Change (CC) message to the output.

        :param channel: MIDI channel (0-15).
        :param data1: Control number (0-127).
        :param data2: Control value (0-127).
        """
        try:
            message = mido.Message('control_change', channel=channel, control=data1, value=data2)
            self.output_port.send(message)
            print(f"Control Change sent - Channel: {channel}, Control: {data1}, Value: {data2}")
        except Exception as e:
            print(f"Error sending Control Change: {e}")

    def send_sysex(self, data):
        """
        Sends a SysEx (System Exclusive) message to the output.

        :param data: List of SysEx data bytes.
        """
        try:
            # Ensure the SysEx message starts and ends correctly
            if data[0] != 0xF0 or data[-1] != 0xF7:
                raise ValueError("SysEx data must start with 0xF0 and end with 0xF7.")

            message = mido.Message('sysex', data=data)
            self.output_port.send(message)
            print(f"SysEx message sent: {data}")
        except Exception as e:
            print(f"Error sending SysEx message: {e}")

    def monitor_device(self):
        """
        Monitors MIDI device connection and disconnection.
        """
        while True:
            available_ports = mido.get_input_names()
            if self.input_name not in available_ports:
                print(f"Device {self.input_name} disconnected!")
                self.stop_receiving()
                self.input_port = None
                self.output_port = None
                self.connect_ports()  # Reconnect when device is available
                self.start_receiving()  # Resume receiving after reconnecting
            time.sleep(2)

    def start_monitoring(self):
        """
        Starts monitoring device connection in a separate thread.
        """
        threading.Thread(target=self.monitor_device, daemon=True).start()
        print("MIDI monitoring thread started.")

    def close(self):
        """
        Closes the MIDI ports.
        """
        if self.input_port:
            self.input_port.close()
        if self.output_port:
            self.output_port.close()
        print("MIDI ports closed.")

#
# ampero = AmperoMP80()
#
#
# # Usage example
# def my_callback(message):
#     ampero.handle_midi(message.data)
#
#
# if __name__ == "__main__":
#     # Replace with the exact names of your MIDI input and output ports
#     # input_name = "HOTONE MP80 PRODUCT 0"
#     # output_name = "HOTONE MP80 PRODUCT 1"
#
#     input_name = "HOTONE MP80 PRODUCT:HOTONE MP80 PRODUCT MIDI 1 20:0"
#     output_name = "HOTONE MP80 PRODUCT:HOTONE MP80 PRODUCT MIDI 1 20:0"
#
#     try:
#         midi_controller = MidiController(input_name, output_name, my_callback)
#         midi_controller.connect_ports()
#         midi_controller.start_receiving()
#         midi_controller.start_monitoring()
#
#         input("Press Enter to exit...\n")
#         midi_controller.close()
#     except Exception as e:
#         print(f"Error: {e}")