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
    SNR: float = 100.0 # не реализовано
    

def LoadFile(path):
    parser = MySpiceParser(path = path)
    circuit = parser.build_circuit();
    return circuit


def SaveFile(analysis, path):
    with open(path, 'w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(numpy.array(analysis.input_dummy, dtype=float))
        csv_writer.writerow(numpy.array(analysis.VCurrent, dtype=float))
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
    analysis = simulator.transient(step_time=period / lendata, end_time=period)
    return analysis
