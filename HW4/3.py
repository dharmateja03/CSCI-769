import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer  

from qiskit.primitives import Sampler
from qiskit.circuit.library import QFT

def create_qpe_circuit(n_count, n_state):
    
    qc = QuantumCircuit(n_count + n_state, n_count)
    
    qc.x(n_count)
    
    for qubit in range(n_count):
        qc.h(qubit)
    
    
    phase = np.pi / 4  # example phase
    
    for i in range(n_count):
        reps = 2**i
        for _ in range(reps):
            # Controlled phase rotation
            qc.cp(phase, i, n_count)
    
    # Apply inverse QFT to counting qubits
    qc.append(QFT(n_count).inverse(), range(n_count))
    
    # Measure counting qubits
    qc.measure(range(n_count), range(n_count))
    
    return qc

# Function to create the inverse QPE circuit
def create_inverse_qpe_circuit(original_qpe):
    
    n_qubits = original_qpe.num_qubits
    
    inverse_qc = QuantumCircuit(n_qubits)
    circuit_no_measure = QuantumCircuit(n_qubits)
    for inst, qargs, _ in original_qpe.data:
        if inst.name != 'measure':
            circuit_no_measure.append(inst, qargs)
    
    # Create the inverse by taking the adjoint (dagger)
    inverse_qc = circuit_no_measure.inverse()
    
    return inverse_qc

# Function to demonstrate that U†U|0⟩|u⟩ = |0⟩|u⟩
def demonstrate_unitarity(n_count, n_state):
    
    original_qpe = create_qpe_circuit(n_count, n_state)
    
    qpe_no_measure = QuantumCircuit(original_qpe.num_qubits)
    for inst, qargs, _ in original_qpe.data:
        if inst.name != 'measure':
            qpe_no_measure.append(inst, qargs)
    
    # Create the inverse QPE circuit
    inverse_qpe = create_inverse_qpe_circuit(original_qpe)
    
    demo_circuit = QuantumCircuit(original_qpe.num_qubits, n_count)
    
    demo_circuit = demo_circuit.compose(qpe_no_measure)
    demo_circuit.barrier()
    
    demo_circuit = demo_circuit.compose(inverse_qpe)
    
    demo_circuit.measure(range(n_count), range(n_count))
    
    return demo_circuit, qpe_no_measure, inverse_qpe

# Main execution
n_count = 3  # Number of counting qubits
n_state = 1  # Number of state qubits (for |u⟩)

original_qpe = create_qpe_circuit(n_count, n_state)
print("Original QPE Circuit:")
print(original_qpe.draw())

inverse_qpe = create_inverse_qpe_circuit(original_qpe)
print("\nInverse QPE Circuit (U†):")
print(inverse_qpe.draw())

demo_circuit, qpe_no_measure, inverse_qpe_clean = demonstrate_unitarity(n_count, n_state)
print("\nFull Demonstration Circuit (U†U|0⟩|u⟩ = |0⟩|u⟩):")
print(demo_circuit.draw())

simulator = Aer.get_backend('statevector_simulator')
transpiled_circuit = transpile(demo_circuit, simulator)
sampler = Sampler()
job = sampler.run([transpiled_circuit], shots=1024)
result = job.result()
counts = result.quasi_dists[0].binary_probabilities()

print("\nSimulation Results:")
for outcome, probability in counts.items():
    print(f"Outcome: |{outcome}⟩, Probability: {probability:.4f}")

zeros_state = '0' * n_count
if zeros_state in counts:
    if counts[zeros_state] > 0.9:  # Allow for some numerical error
        print(f"\nDemonstration successful! Probability of measuring |{zeros_state}⟩: {counts[zeros_state]:.4f}")
        print("This confirms that U†U|0⟩|u⟩ = |0⟩|u⟩")
    else:
        print(f"\nDemonstration uncertain. Probability of measuring |{zeros_state}⟩: {counts[zeros_state]:.4f}")
else:
    print("\nDemonstration failed. State |000⟩ not measured.")

