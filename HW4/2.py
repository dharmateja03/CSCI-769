
from qiskit_aer import Aer  

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import Sampler
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

n = 3
shots = 100

def create_oracle_min():
    oracle = QuantumCircuit(n)
    
    for i in range(n):
        oracle.x(i)
    
    
    oracle.h(n-1)
    oracle.mcx(list(range(n-1)), n-1)  
    oracle.h(n-1)
    
    for i in range(n):
        oracle.x(i)
        
    return oracle

def create_oracle_max():
    oracle = QuantumCircuit(n)
    
   
    oracle.h(n-1)
    oracle.mcx(list(range(n-1)), n-1)  
    oracle.h(n-1)
        
    return oracle

def create_diffusion():
    diffusion = QuantumCircuit(n)
    
    for i in range(n):
        diffusion.h(i)
    
    for i in range(n):
        diffusion.x(i)
    
    diffusion.h(n-1)
    diffusion.mcx(list(range(n-1)), n-1)  
    diffusion.h(n-1)
    
    # Apply X gates to all qubits
    for i in range(n):
        diffusion.x(i)
    
    # Apply H gates to all qubits
    for i in range(n):
        diffusion.h(i)
    
    return diffusion

def run_grover(oracle_func, iterations, target_state):
    qc = QuantumCircuit(n, n)
    
    for i in range(n):
        qc.h(i)
    
    oracle = oracle_func()
    diffusion = create_diffusion()
    
    for _ in range(iterations):
        qc = qc.compose(oracle)
        qc = qc.compose(diffusion)
    
    qc.measure(range(n), range(n))
    
    # Get the circuit depth
    depth = qc.depth()
    simulator = Aer.get_backend('qasm_simulator')
    qc_transpiled = transpile(qc, simulator)
    
    sampler = Sampler()
    job = sampler.run(qc_transpiled, shots=shots)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()
    
    # Calculate probability of the target state
    if target_state in counts:
        target_prob = counts[target_state]
    else:
        target_prob = 0
    
    return qc, counts, target_prob, depth

iterations_list = [2, 3, 8]
target_min = '000'
target_max = '111'

min_results = []
max_results = []

# Run for minimum (|000⟩)
print("Grover's Algorithm for finding |000⟩ (minimum):")
print("===============================================")
for iterations in iterations_list:
    print(f"\nRunning with {iterations} iterations:")
    qc_min, counts_min, prob_min, depth_min = run_grover(create_oracle_min, iterations, target_min)
    min_results.append((iterations, counts_min, prob_min, depth_min))
    print(f"Circuit depth: {depth_min}")
    print(f"Probability of measuring |{target_min}⟩: {prob_min:.4f}")
    print(f"Counts: {counts_min}")

# Run for maximum (|111⟩)
print("\nGrover's Algorithm for finding |111⟩ (maximum):")
print("===============================================")
for iterations in iterations_list:
    print(f"\nRunning with {iterations} iterations:")
    qc_max, counts_max, prob_max, depth_max = run_grover(create_oracle_max, iterations, target_max)
    max_results.append((iterations, counts_max, prob_max, depth_max))
    print(f"Circuit depth: {depth_max}")
    print(f"Probability of measuring |{target_max}⟩: {prob_max:.4f}")
    print(f"Counts: {counts_max}")

# Calculate the optimal number of iterations
print("\nOptimal Number of Iterations Analysis:")
print("====================================")
N = 2**n
optimal_iterations = np.pi/4 * np.sqrt(N)
print(f"For n={n}, optimal iterations ≈ {optimal_iterations:.2f}")

# Plot the results
plt.figure(figsize=(10, 6))
iterations_array = np.array(iterations_list)
min_probs = [result[2] for result in min_results]
max_probs = [result[2] for result in max_results]

plt.plot(iterations_array, min_probs, 'o-', label=f'Minimum (|{target_min}⟩)')
plt.plot(iterations_array, max_probs, 's-', label=f'Maximum (|{target_max}⟩)')
plt.axvline(x=optimal_iterations, color='r', linestyle='--', label=f'Optimal ({optimal_iterations:.2f})')
plt.xlabel('Number of Iterations')
plt.ylabel('Probability of Target State')
plt.title("Effect of Iteration Count on Target State Probability")
plt.xticks(iterations_array)
plt.ylim(0, 1)
plt.grid(True)
plt.legend()
plt.savefig('grover_iterations_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Create a table with the results
print("\nResults Summary Table:")
print("=====================")
print(f"{'Iterations':<12}{'|000⟩ Prob':<15}{'|000⟩ Depth':<15}{'|111⟩ Prob':<15}{'|111⟩ Depth':<15}")
print("-" * 72)
for i in range(len(iterations_list)):
    print(f"{iterations_list[i]:<12}{min_results[i][2]:<15.4f}{min_results[i][3]:<15}{max_results[i][2]:<15.4f}{max_results[i][3]:<15}")

print("\nSaving circuit text representations instead of images")
min_circuit, _, _, _ = run_grover(create_oracle_min, 1, target_min)
max_circuit, _, _, _ = run_grover(create_oracle_max, 1, target_max)
print("Minimum circuit:")
print(min_circuit)

print("\nMaximum circuit:")
print(max_circuit)
