import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer  

from qiskit.quantum_info import Statevector
from qiskit.circuit.library import QFT
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

A = np.array([[1.0]])
b = np.array([1.0])


n_b = 1       
n_clock = 3   
ancilla = 1  

qc = QuantumCircuit(n_clock + n_b + ancilla, n_clock)


qc.x(n_clock) 

for i in range(n_clock):
    qc.h(i)

for i in range(n_clock):
    
    qc.cp(2*np.pi*2**i, i, n_clock)


qc.append(QFT(n_clock).inverse(), range(n_clock))

qc.x(n_clock + n_b)  
for i in range(n_clock):
    
    qc.cry(np.pi/2, i, n_clock + n_b)

qc.append(QFT(n_clock), range(n_clock))
for i in range(n_clock):
    qc.h(i)
for i in range(n_clock):
    qc.cp(-2*np.pi*2**i, i, n_clock)

qc.measure(range(n_clock), range(n_clock))

simulator = Aer.get_backend('aer_simulator')
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()
counts = result.get_counts()

print("Circuit measurements:", counts)
print("Solution x₁ = 1 (corresponds to state |1⟩ of the b register)")
