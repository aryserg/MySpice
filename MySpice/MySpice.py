import math
import csv
import argparse
import numpy
from dataclasses import dataclass

from PySpice.Spice.Parser import SpiceParser
from PySpice.Spice.Parser import Model
from PySpice.Spice.Parser import Element
from PySpice.Unit import *


# Переопределяем парсер spice так чтобы он игнорировал секции .include и .subckt
class MySpiceParser(SpiceParser):    
    @staticmethod
    def _build_circuit(circuit, statements, ground):        
        for statement in statements:
            if isinstance(statement, Element):
                statement.build(circuit, ground)
            elif isinstance(statement, Model):
               statement.build(circuit)


@dataclass
class Init_Data:
    F: float
    V: float
    Rcs: float = 0.0
    SNR: float = 40.0  
    

def LoadFile(path):
    parser = MySpiceParser(path = path)
    circuit = parser.build_circuit();
    return circuit


def SaveFile(analysis, path):
    with open(path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter = ';')
        csv_writer.writerow(analysis.input_dummy)
        csv_writer.writerow(analysis.VCurrent)
    return

    
def CreateCVC(circuit, input_data, lendata ):
    # lendata не может принимать значения меньше 59
    #if lendata>86:
    #    lendata = lendata - 8
    #else:
    #    lendata = lendata - 9    
    period = 1 / input_data.F
    rms_voltage = input_data.V / math.sqrt(2)
    circuit.R('cs', 'input', 'input_dummy', input_data.Rcs)
    circuit.AcLine('Current', circuit.gnd, 'input_dummy', rms_voltage = rms_voltage, frequency = input_data.F)
    simulator = circuit.simulator()
    analysis = simulator.transient(step_time = period / lendata, end_time = period)
# Расчитываем шум независмо для тока и напряжения исходя из среднеквадратичных значений и одинакового SNR    
    avg_V_db = 10 * numpy.log10(numpy.mean(numpy.array(analysis.input_dummy, dtype = float) ** 2))
    avg_Vnoise_db = avg_V_db - input_data.SNR
    Vnoise = numpy.random.normal(0, numpy.sqrt(10 ** (avg_Vnoise_db / 10)), len(analysis.input_dummy))
    analysis.input_dummy = numpy.array(analysis.input_dummy, dtype = float) + Vnoise
    avg_I_db = 10 * numpy.log10(numpy.mean(numpy.array(analysis.VCurrent, dtype = float) ** 2))
    avg_Inoise_db = avg_I_db - input_data.SNR
    Inoise = numpy.random.normal(0, numpy.sqrt(10 ** (avg_Inoise_db / 10)), len(analysis.input_dummy))
    analysis.VCurrent = numpy.array(analysis.VCurrent, dtype = float) + Inoise
    return analysis
