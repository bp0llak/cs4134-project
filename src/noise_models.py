from qiskit_aer.noise import NoiseModel, QuantumError, pauli_error
from qiskit import QuantumCircuit
from qiskit.circuit.library import IGate, XGate, ZGate

def bit_flip_noise_model(p):
    """NoiseModel to bit flip qubit with probability p on single-qubit gate"""
    nm = NoiseModel()
    noise_op = [(IGate(), 1-p), (XGate(), p)]
    qerr = QuantumError(noise_op)
    nm.add_all_qubit_quantum_error(qerr, ['u1','u2','u3','x','sx','id','reset','rz','u'])
    # nm.add_all_qubit_quantum_error(qerr, ['measure'])
    return nm

def phase_flip_noise_model(p):
    """NoiseModel to phase flip qubit with probability p on single-qubit gate"""
    nm = NoiseModel()
    noise_op = [(IGate(), 1-p), (ZGate(), p)]
    qerr = QuantumError(noise_op)
    nm.add_all_qubit_quantum_error(qerr, ['u1','u2','u3','x','sx','id','reset','rz','u'])
    # nm.add_all_qubit_quantum_error(qerr, ['measure'])
    return nm

def mixed_noise_model(p_x, p_z):
    """NoiseModel to apply pauli_error on qubit with probability p_x/p_z on single-qubit gate"""
    nm = NoiseModel()
    qerr = pauli_error([('I', 1-p_x-p_z),('X', p_x),('Z', p_z)])
    nm.add_all_qubit_quantum_error(qerr, ['u1','u2','u3','x','sx','id','reset','rz','u'])
    # nm.add_all_qubit_quantum_error(qerr, ['measure'])
    return nm