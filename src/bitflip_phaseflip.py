from qiskit_aer.noise import NoiseModel
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import IGate, XGate, ZGate, HGate


def encode_3qubit_bitflip():
    q = QuantumRegister(3, 'q')
    qc = QuantumCircuit(q)
    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])
    return qc

def decode_3qubit_bitflip():
    q = QuantumRegister(3, 'q')
    qc = QuantumCircuit(q)
    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])
    qc.ccx(q[2], q[1], q[0])
    return qc   # Need to measure after

def encode_3qubit_phaseflip():
    q = QuantumRegister(3, 'q')
    qc = QuantumCircuit(q)
    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])
    qc.h(q[0])
    qc.h(q[1])
    qc.h(q[2])
    return qc

def decode_3qubit_phaseflip():
    q = QuantumRegister(3, 'q')
    qc = QuantumCircuit(q)
    qc.h(q[0])
    qc.h(q[1])
    qc.h(q[2])
    qc.cx(q[0], q[1])
    qc.cx(q[0], q[2])
    qc.ccx(q[2], q[1], q[0])
    return qc   # Need to measure after

def encode_9qubit_shor():
    q = QuantumRegister(9, 'q')
    qc = QuantumCircuit(q)
    qc.cx(q[0], q[3])
    qc.cx(q[0], q[6])
    qc.h(q[0])
    qc.h(q[3])
    qc.h(q[6])
    qc.cx(q[0], q[1])
    qc.cx(q[3], q[4])
    qc.cx(q[6], q[7])
    qc.cx(q[0], q[2])
    qc.cx(q[3], q[5])
    qc.cx(q[6], q[8])
    return qc

def decode_9qubit_shor():
    q = QuantumRegister(9, 'q')
    qc = QuantumCircuit(q)
    qc.cx(q[0], q[1])
    qc.cx(q[3], q[4])
    qc.cx(q[6], q[7])
    qc.cx(q[0], q[2])
    qc.cx(q[3], q[5])
    qc.cx(q[6], q[8])
    qc.ccx(q[1], q[2], q[0])
    qc.ccx(q[4], q[5], q[3])
    qc.ccx(q[8], q[7], q[6])
    qc.h(q[0])
    qc.h(q[3])
    qc.h(q[6])
    qc.cx(q[0], q[3])
    qc.cx(q[0], q[6])
    qc.ccx(q[6], q[3], q[0])
    return qc # Need to measure after
    
    