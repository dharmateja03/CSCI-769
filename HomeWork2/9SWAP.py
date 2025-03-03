#Implementing the SWAP Gate in Qiskit (10 pts)
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def run_swap_circuit(initial_state):
    qc = QuantumCircuit(2)
    if initial_state == '10':
        qc.x(1)
    elif initial_state == '01':
        qc.x(0)
    elif initial_state == '11':
        qc.x(0)
        qc.x(1)
    qc.cx(0, 1)
    qc.cx(1, 0)
    qc.cx(0, 1)
    
    # Simulate 
    state = Statevector.from_instruction(qc)
    probabilities = state.probabilities_dict()
    
    return probabilities

basis_states = ['00', '01', '10', '11']

print("Simulation Results:")
for state in basis_states:
    result = run_swap_circuit(state)
    most_likely_outcome = max(result.items(), key=lambda x: x[1])[0]
    print(f"Initial state: |{state}⟩, Result state: |{most_likely_outcome}⟩, Probabilities: {result}")


