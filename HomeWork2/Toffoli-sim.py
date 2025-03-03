from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt


def create_toffoli_circuit(initial_state):
    
    qc = QuantumCircuit(3, 3)
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
    
    qc.barrier()  
    qc.measure([0, 1, 2], [0, 1, 2])
    
    return qc


simulator = AerSimulator()
basis_states = ['000', '001', '010', '011', '100', '101', '110', '111']
results = {}

print("Toffoli Gate AerSimulator Results (1000 shots):")
print("----------------------------------------------")

for state in basis_states:
    circuit = create_toffoli_circuit(state)
    compiled_circuit = transpile(circuit, simulator)
    
    # Run the circuit on the simulator
    job = simulator.run(compiled_circuit, shots=1000)
    result = job.result()
    counts = result.get_counts()
    results[state] = counts
    
    # Print results
    print(f"Initial state: |{state}⟩")
    print(f"Results: {counts}")
    
    # Calculate accuracy 
    if state == '110':
        expected = '111'
    elif state == '111':
        expected = '110'
    else:
        expected = state
    
    accuracy = counts.get(expected, 0) / 1000 * 100
    print(f"Accuracy for expected outcome |{expected}⟩: {accuracy:.2f}%\n")


example_circuit = create_toffoli_circuit('110')
print("Toffoli Circuit Implementation for initial state |110⟩:")
print(example_circuit.draw(output='text'))
