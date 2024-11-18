import numpy as np

def bpsk_modulation(bits, carrier_freq, sampling_rate = 2000, bit_duration = 0.01) -> np.ndarray:
    """BPSK модуляция на основе синусоидальной волны."""
    t = np.linspace(0, bit_duration, int(sampling_rate * bit_duration), endpoint=False)
    modulated_signal = []
    carrier_wave = np.sin(2 * np.pi * carrier_freq * t)
    # print(carrier_wave)
    for bit in bits:
        modulated_wave = carrier_wave if bit == 1 else -carrier_wave
    #   print(modulated_wave, sep=' ')
        modulated_signal.append(modulated_wave)
    return np.concatenate(modulated_signal), t

def bpsk_demodulation(received_signal, carrier_freq, sampling_rate = 2000, bit_duration = 0.01) -> np.ndarray:
    """BPSK демодуляция на основе синусоидальной волны."""
    t = np.linspace(0, bit_duration, int(sampling_rate * bit_duration), endpoint=False)
    carrier_wave = np.sin(2 * np.pi * carrier_freq * t)
    samples_per_bit = len(carrier_wave)
    demodulated_bits = []
    for i in range(0, len(received_signal), samples_per_bit):
        bit_segment = received_signal[i:i+samples_per_bit]
        correlation = np.sum(bit_segment * carrier_wave)
        demodulated_bits.append(1 if correlation > 0 else -1)
    return np.array(demodulated_bits)
