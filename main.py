from machine import Pin, PWM, time_pulse_us
from time import sleep, sleep_us

# Sensor ultrassonico HC-SR04
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

# Buzzer passivo: produz as notas da melodia
buzzer = PWM(Pin(19), freq=440, duty=0)

# Melodia original simples: (frequencia em Hz, duracao em segundos)
melodia = [
    (262, 0.30), (330, 0.30), (392, 0.30), (523, 0.45),
    (392, 0.30), (330, 0.30), (294, 0.30), (349, 0.45),
    (330, 0.30), (294, 0.30), (262, 0.60), (0, 0.20),
]


def medir_distancia():
    trig.off()
    sleep_us(2)
    trig.on()
    sleep_us(10)
    trig.off()

    pulso = time_pulse_us(echo, 1, 30000)
    if pulso < 0:
        return None
    return pulso / 58.0  # cm (aproximacao)


def obter_velocidade(distancia):
    if distancia is None:
        return 1.0  # distancia invalida: velocidade normal

    # Faixa de 5 a 40 cm; perto = rapido, longe = lento.
    distancia = max(5, min(40, distancia))
    return 2.0 - (distancia - 5) * (1.5 / 35)
    # 5 cm => 2x; 40 cm => 0.5x


print('AirDJ iniciado! Ajuste a distancia do HC-SR04 no Wokwi.')

try:
    while True:
        for frequencia, duracao in melodia:
            distancia = medir_distancia()
            velocidade = obter_velocidade(distancia)
            tempo = duracao / velocidade

            if distancia is None:
                print('Sem leitura: velocidade normal')
            else:
                print('Distancia: {:.1f} cm | Velocidade: {:.2f}x'.format(
                    distancia, velocidade))

            if frequencia > 0:
                buzzer.freq(frequencia)
                buzzer.duty(512)
                sleep(tempo * 0.85)
                buzzer.duty(0)
                sleep(tempo * 0.15)
            else:
                buzzer.duty(0)
                sleep(tempo)
except KeyboardInterrupt:
    buzzer.duty(0)
    buzzer.deinit()
