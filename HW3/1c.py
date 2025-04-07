import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from collections import Counter
def quantum_repetition_code_multiple_rounds(num_rounds=10):
    qc = QuantumCircuit(5, 3 + 2*num_rounds)
    apply_x = np.random.random() < 0.5
    if apply_x:
        qc.x(0)
        print(f"X gate applied to first qubit - starting with |1⟩")
    else:
        print(f"No X gate applied - starting with |0⟩")

    for round_idx in range(num_rounds):
        qc.reset(3)
        qc.reset(4)
        qc.h(3)
        qc.h(4)
        qc.cx(0, 3)
        qc.cx(1, 3)
        qc.cx(1, 4)
        qc.cx(2, 4)
        
        qc.measure(3, 3 + 2*round_idx)     
        qc.measure(4, 3 + 2*round_idx + 1) 
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.measure(2, 2)
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=100)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    return counts

def analyze_results(counts):
    all_syndromes = []
    data_results = {}
    
    for outcome, count in counts.items():
        
        data_bits = outcome[:3] 
        
        syndromes = []
        for i in range(10):  # 10 rounds
            start_idx = 3 + 2*i
            if start_idx + 1 < len(outcome):
                syndrome = outcome[start_idx:start_idx+2]
                syndromes.append(syndrome)
        
        # Count how many times each syndrome appears
        syndrome_counter = Counter(syndromes)
        most_common_syndrome = syndrome_counter.most_common(1)[0][0]
        all_syndromes.append((most_common_syndrome, count))
        if data_bits in data_results:
            data_results[data_bits] += count
        else:
            data_results[data_bits] = count
    syndrome_counts = {}
    for syndrome, count in all_syndromes:
        if syndrome in syndrome_counts:
            syndrome_counts[syndrome] += count
        else:
            syndrome_counts[syndrome] = count
    
    return data_results, syndrome_counts

counts = quantum_repetition_code_multiple_rounds(num_rounds=10)
data_results, syndrome_counts = analyze_results(counts)
print("Data qubit measurements:", data_results)
print("Most common syndrome measurements:", syndrome_counts)
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plot_histogram(data_results)
plt.title("Data Qubit Measurements (After Multiple Rounds)")
plt.subplot(1, 2, 2)
plot_histogram(syndrome_counts)
plt.title("Most Common Syndrome Measurements")

plt.tight_layout()
plt.show()