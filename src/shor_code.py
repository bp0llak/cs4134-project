import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import Aer
from qiskit_aer.noise import NoiseModel

from noise_models import bit_flip_noise_model, phase_flip_noise_model, mixed_noise_model
from bitflip_phaseflip import encode_3qubit_bitflip, encode_3qubit_phaseflip, encode_9qubit_shor
from bitflip_phaseflip import decode_3qubit_bitflip, decode_3qubit_phaseflip, decode_9qubit_shor

def run_qec_test(encode : QuantumCircuit, decode : QuantumCircuit, initial="0", noise_model=None, shots=1024):
    """
    Encodes 0 state, applies error, decodes, and measures output.
    Returns success probability
    """
    nQubits = encode.num_qubits
    q = QuantumRegister(nQubits, 'q')
    c = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(q, c)

    # Prep initial state
    if initial == "1":
        qc.x(q[0])
    elif initial == "+":
        qc.h(q[0])
    elif initial == "-":
        qc.h(q[0])
        qc.z(q[0])

    # Encode
    qc.append(encode.to_gate(), list(range(nQubits)))

    # Insert noise through identity gate
    qc.barrier()
    for i in range(nQubits):
        qc.id(i)
    
    # Decode
    qc.barrier()
    qc.append(decode.to_gate(), list(range(nQubits)))

    if initial in ("+", "-"):
        qc.h(q[0])

    qc.measure(q[0], c[0])

    sim = Aer.get_backend('qasm_simulator')
    transpiled = transpile(qc, sim, optimization_level=0)
    # print(transpiled) # Used for testing circuit visually
    job = sim.run(transpiled, noise_model=noise_model, shots=shots)


    result = job.result()
    counts = result.get_counts()

    target = "0" if initial in ("0", "+") else "1"

    return counts.get(target, 0) / shots


def drawCircuit(encode : QuantumCircuit, decode : QuantumCircuit):
    """
    Draws circuit diagram
    """
    nQubits = encode.num_qubits
    q = QuantumRegister(nQubits, 'q')
    c = ClassicalRegister(1, 'c')
    qc = QuantumCircuit(q, c)

    # Encode
    qc.append(encode.to_gate(), list(range(nQubits)))

    # Insert noise through identity gate
    qc.barrier()
    for i in range(nQubits):
        qc.id(i)
    
    # Decode
    qc.barrier()
    qc.append(decode.to_gate(), list(range(nQubits)))

    qc.measure(q[0], c[0])

    if (nQubits == 9):
        qc.draw(output='mpl', filename='shorcode.png')
    elif (nQubits == 3):
        qc.draw(output='mpl', filename='code_diagram.png')


if __name__ == "__main__":
    p = 0.2
    noise_none = None
    noise_bit = bit_flip_noise_model(p=p)
    noise_phase = phase_flip_noise_model(p=p)
    noise_mixed = mixed_noise_model(p_x=0.1,p_z=0.1)

    print("3-Qubit |0> Bit-Flip Code (no noise):", run_qec_test(encode_3qubit_bitflip(), decode_3qubit_bitflip(), noise_model=noise_none))
    print("3-Qubit |0> Bit-Flip Code (bit-flip noise p=0.2):", run_qec_test(encode_3qubit_bitflip(), decode_3qubit_bitflip(), noise_model=noise_bit))
    print("3-Qubit |1> Bit-Flip Code (bit-flip noise p=0.2):", run_qec_test(encode_3qubit_bitflip(), decode_3qubit_bitflip(), initial="1", noise_model=noise_bit))
    print("3-Qubit |0> Bit-Flip Code (phase-flip noise p=0.2):", run_qec_test(encode_3qubit_bitflip(), decode_3qubit_bitflip(), noise_model=noise_phase))
    print("3-Qubit |1> Bit-Flip Code (phase-flip noise p=0.2):", run_qec_test(encode_3qubit_bitflip(), decode_3qubit_bitflip(), initial="1", noise_model=noise_phase))
    #print("3-Qubit Bit-Flip Code (mixed noise p_x/z=0.2):", run_qec_test(encode_3qubit_bitflip(), decode_3qubit_bitflip(), noise_mixed))

    print("3-Qubit |0> Phase-Flip Code (no noise):", run_qec_test(encode_3qubit_phaseflip(), decode_3qubit_phaseflip(), noise_model=noise_none))
    print("3-Qubit |0> Phase-Flip Code (bit-flip noise p=0.2):", run_qec_test(encode_3qubit_phaseflip(), decode_3qubit_phaseflip(), noise_model=noise_bit))
    print("3-Qubit |1> Phase-Flip Code (bit-flip noise p=0.2):", run_qec_test(encode_3qubit_phaseflip(), decode_3qubit_phaseflip(), initial="1", noise_model=noise_bit))
    print("3-Qubit |0> Phase-Flip Code (phase-flip noise p=0.2):", run_qec_test(encode_3qubit_phaseflip(), decode_3qubit_phaseflip(), noise_model=noise_phase))
    print("3-Qubit |1> Phase-Flip Code (phase-flip noise p=0.2):", run_qec_test(encode_3qubit_phaseflip(), decode_3qubit_phaseflip(), initial="1", noise_model=noise_phase))

    print("=== SHOR CODE (9-qubit) ===")
    print("No noise:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), noise_model=noise_none))
    print("Bit-Flip |0>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), noise_model=noise_bit))
    print("Bit-Flip |1>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="1", noise_model=noise_bit))
    print("Bit-Flip |+>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="+", noise_model=noise_bit))
    print("Bit-Flip |->:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="-", noise_model=noise_bit))

    print("Phase-Flip |0>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), noise_model=noise_phase))
    print("Phase-Flip |1>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="1", noise_model=noise_phase))
    print("Phase-Flip |+>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="+", noise_model=noise_phase))
    print("Phase-Flip |->:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="-", noise_model=noise_phase))

    print("Mixed-noise |0>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), noise_model=noise_mixed))
    print("Mixed-noise |1>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="1", noise_model=noise_mixed))
    print("Mixed-noise |+>:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="+", noise_model=noise_mixed))
    print("Mixed-noise |->:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), initial="-", noise_model=noise_mixed))

    # print("Mixed-noise:", run_qec_test(encode_9qubit_shor(), decode_9qubit_shor(), noise_model=noise_mixed))