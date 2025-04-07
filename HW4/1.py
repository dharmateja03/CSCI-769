import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit_aer import Aer  


num_shots = 20

def dj_f_x0_equals_0():
    # For this function, we need 1 input qubit + 1 output qubit
    qc = QuantumCircuit(2, 1)
    
    qc.x(1)
    qc.h(0)
    qc.h(1)
    
    qc.h(0)
    
    # Measure the input qubit
    qc.measure(0, 0)
    
    return qc

def dj_f_x0_xor_x1():
    qc = QuantumCircuit(3, 2)

    qc.x(2)
    
    qc.h(0)
    qc.h(1)
    qc.h(2)
    
    qc.cx(0, 2)
    qc.cx(1, 2)
    
    qc.h(0)
    qc.h(1)
    
    qc.measure([0, 1], [0, 1])
    
    return qc

def dj_f_x0_equals_x0():
    qc = QuantumCircuit(2, 1)
    
    qc.x(1)
    
    qc.h(0)
    qc.h(1)
  
    qc.cx(0, 1)
    
    # Apply Hadamard to input qubit
    qc.h(0)
    
    # Measure the input qubit
    qc.measure(0, 0)
    
    return qc

# 4. Function f(x₀, x₁) = 1 (Constant function)
def dj_f_constant_1():
    qc = QuantumCircuit(3, 2)
    
    qc.x(2)
    
    qc.h(0)
    qc.h(1)
    qc.h(2)
    
    qc.z(2)
   
    qc.h(0)
    qc.h(1)
    
    # Measure the input qubits
    qc.measure([0, 1], [0, 1])
    
    return qc

# Simulate the circuits
def simulate_circuit(qc, name):
    simulator = Aer.get_backend('qasm_simulator')
    sampler = Sampler()
    job = sampler.run(qc, shots=num_shots)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()
    
    print(f"Simulation results for {name}:")
    print(counts)
    
    # Determine if constant or balanced
    num_input_qubits = qc.num_qubits - 1  # Subtract the auxiliary qubit
    if '0' * num_input_qubits in counts and counts['0' * num_input_qubits] > 0.9:
        print("Function is likely CONSTANT")
    else:
        print("Function is likely BALANCED")
    
    return counts

# Run on simulator
f1_circuit = dj_f_x0_equals_0()
f2_circuit = dj_f_x0_xor_x1()
f3_circuit = dj_f_x0_equals_x0()
f4_circuit = dj_f_constant_1()

print("Deutsch-Jozsa Algorithm Implementations")
print("======================================")

print("\nCircuit for f(x₀) = 0:")
print(f1_circuit)
result1 = simulate_circuit(f1_circuit, "f(x₀) = 0")

print("\nCircuit for f(x₀, x₁) = x₀ ⊕ x₁:")
print(f2_circuit)
result2 = simulate_circuit(f2_circuit, "f(x₀, x₁) = x₀ ⊕ x₁")

print("\nCircuit for f(x₀) = x₀:")
print(f3_circuit)
result3 = simulate_circuit(f3_circuit, "f(x₀) = x₀")

print("\nCircuit for f(x₀, x₁) = 1:")
print(f4_circuit)
result4 = simulate_circuit(f4_circuit, "f(x₀, x₁) = 1")

