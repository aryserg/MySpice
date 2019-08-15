
import matplotlib.pyplot as plt

import PySpice.Logging.Logging as Logging

from MySpice import MySpice as spice

logger = Logging.setup_logging()
circuit = spice.LoadFile('пример3.cir')
input_data = spice.Init_Data(1000, 0.3)
analysis = spice.CreateCVC(circuit, input_data, 100)
spice.SaveFile(analysis, "пример3.csv")

figure1 = plt.figure(1, (20, 10))
plt.grid()
plt.plot(analysis.input_dummy, analysis.VCurrent)
plt.xlabel('Напряжение [В]')
plt.ylabel('Сила тока [А]')
plt.show()
