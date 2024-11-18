import numpy as np
import matplotlib.pyplot as plt


def draw(combined_signal, sampling_rate):
    plt.figure(figsize=(10, 5))
    plt.plot(np.arange(len(combined_signal)) / sampling_rate, combined_signal)
    plt.title("Результирующий сигнал после интерференции (CDMA + BPSK)")
    plt.xlabel("Время (с)")
    plt.ylabel("Амплитуда")
    plt.grid()
    plt.show()