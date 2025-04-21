from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer  
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.primitives import Sampler
import numpy as np
import matplotlib.pyplot as plt
from math import gcd
from fractions import Fraction


N = 15  
a = 2   

n_count = 8  
n_input = 4 

def qft_dagger(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    for j in range(n):
        for m in range(j):
            circuit.cp(-np.pi/float(2**(j-m)), m, j)
        circuit.h(j)
    return circuit

def c_amod15(a, power):
    U = QuantumCircuit(4)
    for iteration in range(power):
        if a == 2:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
    return U

def create_shor_circuit():
    qc = QuantumCircuit(n_count + n_input, n_count)
    
    for q in range(n_count):
        qc.h(q)
    
    qc.x(n_count)
    
    for q in range(n_count):
        power = 2 ** q
        controlled_U = c_amod15(a, power).control(1)
        qc.append(controlled_U, [q] + list(range(n_count, n_count + n_input)))
    
    qft_dagger(qc, n_count)
    
    qc.measure(range(n_count), range(n_count))
    
    return qc

def find_period_and_factors():
   
    shor_circuit = create_shor_circuit()
    
    simulator = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(shor_circuit, simulator)
    
    sampler = Sampler()
    job = sampler.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.quasi_dists[0]
    formatted_counts = {}
    for key, value in counts.items():
        binary_key = format(key, f'0{n_count}b')
        formatted_counts[binary_key] = value
    measured_phases = []
    for output, count in formatted_counts.items():
        decimal = int(output, 2)
        phase = decimal/(2**n_count)
        measured_phases.append((phase, count))
    measured_phases.sort(key=lambda x: x[1], reverse=True)
    
    for phase, count in measured_phases:
        if phase != 0:  
            frac = Fraction(phase).limit_denominator(N)
            r = frac.denominator
            if pow(a, r, N) == 1:
                # factors
                if r % 2 == 0:
                    a_r_div_2 = pow(a, r // 2, N)
                    factor1 = gcd(a_r_div_2 + 1, N)
                    factor2 = gcd(a_r_div_2 - 1, N)
                    
                    if factor1 != 1 and factor1 != N:
                        return r, factor1, factor2
    
    return None, None, None


period, factor1, factor2 = find_period_and_factors()

print(f"For N = {N} and a = {2}:")
print(f"Period found: r = {period}")
print(f"Factors: {factor1} × {factor2} = {N}")
