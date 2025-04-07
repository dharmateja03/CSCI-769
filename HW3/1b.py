import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import random
def quantum_repetition_code():
    qc = QuantumCircuit(5, 5)
    
    apply_x = random.random() < 0.5
    if apply_x:
        qc.x(0)
        print("X gate applied to first qubit - starting with |1⟩")
    else:
        print("No X gate applied - starting with |0⟩")
    
    qc.h(3)
    qc.h(4)
    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.cx(1, 4)
    qc.cx(2, 4)   
    qc.measure(3, 3)
    qc.measure(4, 4)
    
    qc.cx(3, 0)
    qc.x(0).c_if(3, 1)
    qc.cx(4, 2)
    qc.x(2).c_if(4, 1)
    
    qc.cx(3, 1)
    qc.cx(4, 1)
    qc.x(1).c_if(3, 1)
    qc.x(1).c_if(4, 1)
    qc.measure(0, 0)
    qc.measure(1, 1)
    qc.measure(2, 2)
    
    print(qc.draw())
 
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, simulator)
 
    job = simulator.run(compiled_circuit, shots=100)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    return counts

# Run the circuit
counts = quantum_repetition_code()
syndrome_counts = {}
data_counts = {}

for outcome, count in counts.items():
    data_bits = outcome[:3]
    syndrome_bits = outcome[3:]
    
    if syndrome_bits in syndrome_counts:
        syndrome_counts[syndrome_bits] += count
    else:
        syndrome_counts[syndrome_bits] = count
    

    if data_bits in data_counts:
        data_counts[data_bits] += count
    else:
        data_counts[data_bits] = count

print("Data qubit measurements:", data_counts)
print("Syndrome measurements:", syndrome_counts)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plot_histogram(data_counts)
plt.title("Data Qubit Measurements")

plt.subplot(1, 2, 2)
plot_histogram(syndrome_counts)
plt.title("Syndrome Measurements")

plt.tight_layout()
plt.show()