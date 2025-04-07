import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import matplotlib.pyplot as plt
import random

def steane_encoding():
    """circuit that encodes a single qubit into the 7-qubit Steane code"""
    qc = QuantumCircuit(7)
    
    qc.h(0)
    qc.h(1)
    qc.h(3)
    
    qc.cx(0, 2)
    qc.cx(0, 4)
    qc.cx(0, 6)
    
    qc.cx(1, 2)
    qc.cx(1, 5)
    qc.cx(1, 6)
    
    qc.cx(3, 4)
    qc.cx(3, 5)
    qc.cx(3, 6)
    
    return qc

def steane_code_circuit():
    """ Steane code with error detection for both bit and phase flips"""
    
    qc = QuantumCircuit(13, 13)
    
    encoding = steane_encoding()
    
    qc = qc.compose(encoding, qubits=range(7))
    

    apply_x = random.random() < 0.5
    if apply_x:
        qc.x(1) 
        print("X error applied to second qubit (qubit 1)")
    else:
        print("No X error applied")
    
    apply_z = random.random() < 0.5
    if apply_z:
        qc.z(1)  
        print("Z error applied to second qubit (qubit 1)")
    else:
        print("No Z error applied")
    
    for i in range(7, 10):
        qc.h(i)
    qc.cx(0, 7)
    qc.cx(2, 7)
    qc.cx(4, 7)
    qc.cx(6, 7)
    qc.cx(1, 8)
    qc.cx(2, 8)
    qc.cx(5, 8)
    qc.cx(6, 8)
    
    qc.cx(3, 9)
    qc.cx(4, 9)
    qc.cx(5, 9)
    qc.cx(6, 9)

    for i in range(7, 10):
        qc.measure(i, i)
    
    for i in range(7):
        qc.h(i)
    
    for i in range(10, 13):
        qc.h(i)

    qc.cx(0, 10)
    qc.cx(2, 10)
    qc.cx(4, 10)
    qc.cx(6, 10)
    qc.cx(1, 11)
    qc.cx(2, 11)
    qc.cx(5, 11)
    qc.cx(6, 11)
   
    qc.cx(3, 12)
    qc.cx(4, 12)
    qc.cx(5, 12)
    qc.cx(6, 12)
   
    for i in range(10, 13):
        qc.measure(i, i)
   
    for i in range(7):
        qc.h(i)
    
    for i in range(7):
        qc.measure(i, i)
    
    return qc, apply_x, apply_z

def run_on_simulator(qc, shots=100):
    simulator = Aer.get_backend('qasm_simulator')
    transpiled_circuit = transpile(qc, simulator)
    job = simulator.run(transpiled_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts(transpiled_circuit)
    return counts

def analyze_results(counts):
    bit_flip_syndromes = {}
    phase_flip_syndromes = {}
    data_qubit_states = {}
    
    for outcome, count in counts.items():
        data_bits = outcome[:7]       
        bit_syndrome = outcome[7:10]  
        phase_syndrome = outcome[10:] 
        
        if bit_syndrome in bit_flip_syndromes:
            bit_flip_syndromes[bit_syndrome] += count
        else:
            bit_flip_syndromes[bit_syndrome] = count
        
        if phase_syndrome in phase_flip_syndromes:
            phase_flip_syndromes[phase_syndrome] += count
        else:
            phase_flip_syndromes[phase_syndrome] = count
        
        if data_bits in data_qubit_states:
            data_qubit_states[data_bits] += count
        else:
            data_qubit_states[data_bits] = count
    
    return data_qubit_states, bit_flip_syndromes, phase_flip_syndromes

def plot_results(data_states, bit_syndromes, phase_syndromes):
    plt.figure(figsize=(18, 6))
    
    plt.subplot(1, 3, 1)
    labels = sorted(data_states.keys())
    values = [data_states[label] for label in labels]
    plt.bar(range(len(values)), values)
    plt.xticks(range(len(values)), labels, rotation=90, fontsize=8)
    plt.xlabel('Data Qubit State')
    plt.ylabel('Count')
    plt.title('Data Qubit Measurements')
    plt.grid(axis='y', alpha=0.3)
    
    plt.subplot(1, 3, 2)
    labels = sorted(bit_syndromes.keys())
    values = [bit_syndromes[label] for label in labels]
    plt.bar(range(len(values)), values)
    plt.xticks(range(len(values)), labels)
    plt.xlabel('Bit Flip Syndrome')
    plt.ylabel('Count')
    plt.title('Bit Flip Syndrome Measurements')
    plt.grid(axis='y', alpha=0.3)
    plt.subplot(1, 3, 3)
    labels = sorted(phase_syndromes.keys())
    values = [phase_syndromes[label] for label in labels]
    plt.bar(range(len(values)), values)
    plt.xticks(range(len(values)), labels)
    plt.xlabel('Phase Flip Syndrome')
    plt.ylabel('Count')
    plt.title('Phase Flip Syndrome Measurements')
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def main():
    qc, x_applied, z_applied = steane_code_circuit()
    
    print("\nCircuit Information:")
    print(f"X error applied to qubit 1: {x_applied}")
    print(f"Z error applied to qubit 1: {z_applied}")
    
    print("\nRunning on ideal simulator...")
    counts = run_on_simulator(qc, shots=100)
    
    data_states, bit_syndromes, phase_syndromes = analyze_results(counts)
    
    print("\nSummary of Results:")
    print(f"Number of unique data qubit states: {len(data_states)}")
    print(f"Number of unique bit flip syndromes: {len(bit_syndromes)}")
    print(f"Number of unique phase flip syndromes: {len(phase_syndromes)}")
    
    most_common_data = max(data_states.items(), key=lambda x: x[1])
    print(f"Most common data state: {most_common_data[0]} (count: {most_common_data[1]})")
    
    most_common_bit = max(bit_syndromes.items(), key=lambda x: x[1])
    most_common_phase = max(phase_syndromes.items(), key=lambda x: x[1])
    print(f"Most common bit flip syndrome: {most_common_bit[0]} (count: {most_common_bit[1]})")
    print(f"Most common phase flip syndrome: {most_common_phase[0]} (count: {most_common_phase[1]})")
    
    plot_results(data_states, bit_syndromes, phase_syndromes)
    
    print("\nDetailed Analysis:")
    if x_applied and not z_applied:
        expected_bit_syndrome = "110"  
        expected_phase_syndrome = "000"  
        print(f"For X error on qubit 1, expected bit syndrome: {expected_bit_syndrome}")
        print(f"For X error on qubit 1, expected phase syndrome: {expected_phase_syndrome}")
    elif z_applied and not x_applied:
        expected_bit_syndrome = "000"  
        expected_phase_syndrome = "110"  
        print(f"For Z error on qubit 1, expected bit syndrome: {expected_bit_syndrome}")
        print(f"For Z error on qubit 1, expected phase syndrome: {expected_phase_syndrome}")
    elif x_applied and z_applied:
        expected_bit_syndrome = "110"  
        expected_phase_syndrome = "110"  
        print(f"For X and Z errors on qubit 1, expected bit syndrome: {expected_bit_syndrome}")
        print(f"For X and Z errors on qubit 1, expected phase syndrome: {expected_phase_syndrome}")
    else:
        expected_bit_syndrome = "000"  
        expected_phase_syndrome = "000"  
        print(f"For no errors, expected bit syndrome: {expected_bit_syndrome}")
        print(f"For no errors, expected phase syndrome: {expected_phase_syndrome}")
    
    bit_match = most_common_bit[0] == expected_bit_syndrome
    phase_match = most_common_phase[0] == expected_phase_syndrome
    print(f"Bit syndrome matches expected: {bit_match}")
    print(f"Phase syndrome matches expected: {phase_match}")
    
    

if __name__ == "__main__":
    main()