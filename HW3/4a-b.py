import numpy as np
import matplotlib.pyplot as plt
from math import ceil, floor


A = 1  
c = 2  

def calculate_logical_error_rate(d, p, pth):
    """Calculate logical error rate based on code distance, physical error rate, and threshold."""
    pL = A * (p / pth) ** ((d + 1) / 2)
    return pL

def calculate_physical_qubits(d):
    """Calculate the number of physical qubits needed for a logical qubit."""
    Nq = c * (d ** 2)
    return Nq

def calculate_correctable_errors(d):
    """Calculate the number of errors that can be corrected based on code distance."""
    return floor((d - 1) / 2)

def analyze_logical_error_rate_behavior():
    """Analyze how logical error rate behaves as code distance approaches infinity."""
    
    distances = list(range(3, 51, 2))  
    
    p_below_threshold = 1e-3  
    p_above_threshold = 1e-1  
    pth = 1e-2                
    
    pL_below = [calculate_logical_error_rate(d, p_below_threshold, pth) for d in distances]
    pL_above = [calculate_logical_error_rate(d, p_above_threshold, pth) for d in distances]
    
    plt.figure(figsize=(12, 8))
    
    plt.semilogy(distances, pL_below, 'b-o', label=f'p = {p_below_threshold} < pth')
    plt.semilogy(distances, pL_above, 'r-o', label=f'p = {p_above_threshold} > pth')
    
    plt.axhline(y=1.0, color='k', linestyle='--', label='pL = 1 (maximum error)')
    
    plt.axhline(y=pth, color='g', linestyle='--', label=f'pth = {pth}')
    
    plt.xlabel('Code Distance (d)', fontsize=14)
    plt.ylabel('Logical Error Rate (pL)', fontsize=14)
    plt.title('Logical Error Rate vs. Code Distance', fontsize=16)
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.legend(fontsize=12)
    
    plt.savefig('logical_error_rate_behavior.png')
    plt.close()
    
    print("Analysis of Logical Error Rate Behavior (Part a):")
    print("=" * 80)
    print(f"When p < pth (p = {p_below_threshold}, pth = {pth}):")
    print(f"  As d increases from {distances[0]} to {distances[-1]}:")
    print(f"  - pL decreases from {pL_below[0]:.2e} to {pL_below[-1]:.2e}")
    print(f"  - Reduction factor: {pL_below[0]/pL_below[-1]:.2e}x")
    print("\nWhen p > pth (p = {p_above_threshold}, pth = {pth}):")
    print(f"  As d increases from {distances[0]} to {distances[-1]}:")
    print(f"  - pL increases from {pL_above[0]:.2e} to {pL_above[-1]:.2e}")
    print(f"  - Increase factor: {pL_above[-1]/pL_above[0]:.2e}x")
    
    
    
    return distances, pL_below, pL_above


def calculate_requirements_for_applications():
    """Calculate the required resources for different quantum applications."""
    
    applications = {
        "Quantum Materials Simulation": 1e-15,
        "Quantum Chemistry": 1e-12,
        "Optimization Problems": 1e-9
    }
    
    p_values = [1e-3, 1e-4]  
    pth_values = [1e-2, 1e-3]  
    
    print("\nResource Requirements for Different Applications (Part b):")
    print("=" * 105)
    print(f"{'Application':<30} {'p':<8} {'pth':<8} {'d':<6} {'Nq':<8} {'Errors Corrected':<16} {'pL':<10}")
    print("-" * 105)
    
    for app_name, pL_target in applications.items():
        for p in p_values:
            for pth in pth_values:
                if p < pth:
                    
                    
                    log_term = np.log(pL_target / A) / np.log(p / pth)
                    d_min = 2 * log_term - 1
                    
                    d = max(3, 2 * ceil(d_min / 2) + 1)  # Round up to next odd number
                    
                    # Calculate other parameters
                    Nq = calculate_physical_qubits(d)
                    correctable_errors = calculate_correctable_errors(d)
                    pL = calculate_logical_error_rate(d, p, pth)
                    
                    # Print results
                    print(f"{app_name:<30} {p:<8.0e} {pth:<8.0e} {d:<6d} {Nq:<8d} {correctable_errors:<16d} {pL:<10.2e}")
                else:
                    # Error correction doesn't work when p >= pth
                    print(f"{app_name:<30} {p:<8.0e} {pth:<8.0e} {'N/A':<6} {'N/A':<8} {'N/A':<16} {'N/A':<10}")
    
    print("-" * 105)
    
    
    app_names = list(applications.keys())
    scenario_names = []
    qubit_counts = []
    distances = []
    
    for app_name, pL_target in applications.items():
        for p in p_values:
            for pth in pth_values:
                if p < pth:
                    log_term = np.log(pL_target / A) / np.log(p / pth)
                    d_min = 2 * log_term - 1
                    d = max(3, 2 * ceil(d_min / 2) + 1)
                    Nq = calculate_physical_qubits(d)
                    
                    scenario = f"p={p:.0e}, pth={pth:.0e}"
                    scenario_names.append(scenario)
                    qubit_counts.append(Nq)
                    distances.append(d)
    
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 1, 1)
    x = np.arange(len(scenario_names))
    width = 0.25
    
    scenario_per_app = 4  
    
    for i in range(len(app_names)):
        start_idx = i * scenario_per_app
        end_idx = start_idx + scenario_per_app
        plt.bar(x[start_idx:end_idx], qubit_counts[start_idx:end_idx], width, 
                label=app_names[i])
    
    plt.ylabel('Physical Qubits Required (Nq)', fontsize=14)
    plt.title('Physical Qubit Requirements by Application and Error Rates', fontsize=16)
    plt.xticks(x, scenario_names, rotation=45, ha='right')
    plt.yscale('log')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    
    for i in range(len(app_names)):
        start_idx = i * scenario_per_app
        end_idx = start_idx + scenario_per_app
        plt.bar(x[start_idx:end_idx], distances[start_idx:end_idx], width, 
                label=app_names[i])
    
    plt.ylabel('Code Distance (d)', fontsize=14)
    plt.title('Required Code Distance by Application and Error Rates', fontsize=16)
    plt.xticks(x, scenario_names, rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('application_requirements.png')
    plt.close()
    
   

# Run the analyses
if __name__ == "__main__":
    print("Quantum Computing Assignment - Problem 4: Logical Error Rate")
    print("=" * 80)
    
    # Part (a)
    distances, pL_below, pL_above = analyze_logical_error_rate_behavior()
    
    # Part (b)
    calculate_requirements_for_applications()
    
    print("\nPlots have been saved as 'logical_error_rate_behavior.png' and 'application_requirements.png'")