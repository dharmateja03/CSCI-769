import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer  
import matplotlib.pyplot as plt
import random


def random_x_gate_circuit():
    qc = QuantumCircuit(1, 1)
    
    should_apply_x = random.random() < 0.5
    if should_apply_x:
        qc.x(0)  
        print("X gate applied - expecting to measure |1⟩")
    else:
        print("No X gate applied - expecting to measure |0⟩")
    
    qc.measure(0, 0)
    print("Circuit:")
    print(qc.draw())
    
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=100)
    result = job.result()
    counts = result.get_counts(qc)
    
    return counts, should_apply_x

counts, x_applied = random_x_gate_circuit()
print(f"Measurement results: {counts}")

# Plot the results
plt.figure(figsize=(8, 6))
plt.bar(counts.keys(), counts.values())
plt.title(f"Results of {'X Gate Applied' if x_applied else 'No X Gate Applied'}")
plt.xlabel('Measured State')
plt.ylabel('Count')
plt.grid(axis='y')
plt.show()
print("\nRunning 100 separate experiments...")
zeros = 0
ones = 0

simulator = Aer.get_backend('qasm_simulator')

for i in range(100):
    qc = QuantumCircuit(1, 1)
   
    if random.random() < 0.5:
        qc.x(0)
        expected_outcome = '1'
    else:
        expected_outcome = '0'
    
    qc.measure(0, 0)
   
    job = simulator.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts(qc)
    measured_outcome = list(counts.keys())[0]
    
    if measured_outcome == '0':
        zeros += 1
    else:
        ones += 1

print(f"Number of |0⟩ measurements: {zeros}")
print(f"Number of |1⟩ measurements: {ones}")

plt.figure(figsize=(8, 6))
labels = ['|0⟩', '|1⟩']
values = [zeros, ones]
plt.bar(labels, values)
plt.title('Results of 100 Random X Gate Applications')
plt.xlabel('Measured State')
plt.ylabel('Count')
plt.grid(axis='y', alpha=0.75)
plt.show()

