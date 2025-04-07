import time

class Tap:
    def __init__(self, led, foot):
        self.led = led  # Objeto Led
        self.foot = foot  # Objeto Foot
        self.bpm = 0  # Inicialmente o BPM é 0
        self.tap_times = []  # Lista para armazenar os tempos das pisadas
        self.min_bpm = 40  # BPM mínimo
        self.max_bpm = 150  # BPM máximo
        self.is_active = True  # Estado do Tap (ativo ou inativo)

        # Define os callbacks do foot para capturar os eventos
        self.foot._callback_press = self._handle_tap

    def _handle_tap(self):
        """Lida com a pisada do botão e ajusta o BPM."""
        if not self.is_active:
            return  # Não faz nada se o Tap estiver desligado

        current_time = time.time()

        if len(self.tap_times) == 0:
            # Primeira pisada: inicia a contagem
            self.tap_times.append(current_time)
        else:
            # Segunda pisada em diante
            elapsed = current_time - self.tap_times[-1]  # Tempo entre a última pisada
            self.tap_times.append(current_time)

            # Calcula o BPM com base no tempo médio entre as pisadas
            if len(self.tap_times) > 1:
                interval = self.tap_times[-1] - self.tap_times[-2]
                calculated_bpm = 60 / interval

                # Ajusta o BPM para os limites
                self.bpm = self._validate_bpm(calculated_bpm)

        # Reinicia o estado se o tempo entre as pisadas for muito longo
        if len(self.tap_times) > 1 and current_time - self.tap_times[-1] > 2:
            self.tap_times.clear()
            self.bpm = 0

        # Atualiza o LED para piscar na nova velocidade
        self._update_led()

    def _validate_bpm(self, bpm):
        """Valida o BPM, ajustando para os limites mínimo e máximo."""
        if bpm < self.min_bpm:
            return self.min_bpm
        elif bpm > self.max_bpm:
            return self.max_bpm
        return int(bpm)

    def _update_led(self):
        """Atualiza o LED para piscar de acordo com o BPM."""
        if self.is_active and self.bpm > 0:
            interval = 60 / self.bpm
            self.led.on()
            time.sleep(interval / 2)  # O LED fica ligado metade do tempo
            self.led.off()
        else:
            self.led.off()

    def set_bpm(self, bpm):
        """Define manualmente o BPM atual."""
        self.bpm = self._validate_bpm(bpm)
        self._update_led()

    def get_bpm(self):
        """Retorna o BPM atual."""
        return self.bpm

    def get_led_pin(self):
        """Retorna o número do pino associado ao LED."""
        return self.led.pin()

    def get_foot_pin(self):
        """Retorna o número do pino associado ao botão (Foot)."""
        return self.foot.get_pin()

    def turn_off(self):
        """Desliga o Tap, fazendo o LED ficar apagado."""
        self.is_active = False
        self.led.off()  # Garante que o LED está desligado

    def turn_on(self):
        """Liga o Tap, permitindo que o LED volte a piscar na velocidade atual."""
        self.is_active = True
        self._update_led()