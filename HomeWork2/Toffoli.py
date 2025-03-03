from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def run_toffoli_circuit(initial_state):
    qc = QuantumCircuit(3)
    
    
    if initial_state[0] == '1':
        qc.x(0)  
    if initial_state[1] == '1':
        qc.x(1)  
    if initial_state[2] == '1':
        qc.x(2)  
    
    qc.barrier()  
    qc.h(2)
    qc.cx(1, 2)
    qc.tdg(2)
    qc.cx(0, 2)
    qc.t(2)
    qc.cx(1, 2)
    qc.tdg(2)
    qc.cx(0, 2)
    qc.t(2)
    qc.h(2)
    qc.t(1)
    qc.cx(0, 1)
    qc.tdg(1)
    qc.cx(0, 1)
  
    qc.t(0)

    state = Statevector.from_instruction(qc)
    probabilities = state.probabilities_dict()
 
    formatted_results = {}
    for bitstring, prob in probabilities.items():
        if prob > 0.001:  # Only include non-zero probabilities
            # Convert from binary to string with leading zeros
            formatted_bitstring = format(int(bitstring, 2), '03b')
            formatted_results[formatted_bitstring] = prob
    
    return formatted_results, qc

# Run for all 8 basis states
basis_states = ['000', '001', '010', '011', '100', '101', '110', '111']

print("Toffoli Gate Simulation Results:")
print("--------------------------------")

for state in basis_states:
    result, _ = run_toffoli_circuit(state)
    
    most_likely_outcome = max(result.items(), key=lambda x: x[1])[0]
   
    dominant_prob = result[most_likely_outcome]
    
    print(f"Initial state: |{state}⟩")
    print(f"Result state: |{most_likely_outcome}⟩ with probability {dominant_prob:.6f}")
    other_probs = {k: v for k, v in result.items() if v > 0.001 and k != most_likely_outcome}
    if other_probs:
        print(f"Other outcomes: {other_probs}")
    print()

_, example_circuit = run_toffoli_circuit('110')
print("Circuit for initial state |110⟩:")
print(example_circuit.draw(output='text'))
