from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
# FIXED: Replaced the old 'Sampler' with the new 'StatevectorSampler'
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.applications import Maxcut
from qiskit_optimization.algorithms import MinimumEigenOptimizer
import networkx as nx
import numpy as np

def solve_logistics_problem(edges):
    """
    The Product: A Quantum Optimizer.
    Input: A list of connections (e.g., [(0,1), (1,2)] representing routes or conflicts)
    Output: The optimal grouping (0 or 1) for each node.
    """
    print(f"1. Building Graph Model from {len(edges)} connections...")
    
    # 1. Define the Problem (The Math)
    num_nodes = max(max(u, v) for u, v in edges) + 1
    graph = nx.Graph()
    graph.add_nodes_from(range(num_nodes))
    graph.add_edges_from(edges)
    
    # 2. Convert to Quantum Physics (Ising Hamiltonian)
    max_cut = Maxcut(graph)
    qp = max_cut.to_quadratic_program()
    
    # 3. Setup the Quantum Solver (QAOA)
    print("2. Spooling up QAOA (Quantum Approximate Optimization Algorithm)...")
    optimizer = COBYLA(maxiter=50)
    
    # FIXED: Use the new V2 Sampler
    sampler = StatevectorSampler() 
    
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=1)
    
    # 4. Run the Optimization
    algorithm = MinimumEigenOptimizer(qaoa)
    result = algorithm.solve(qp)
    
    print("3. Optimization Complete.")
    
    # 5. Decode the Result
    solution = result.x 
    
    # Format the output for humans
    group_a = [i for i, val in enumerate(solution) if val == 0]
    group_b = [i for i, val in enumerate(solution) if val == 1]
    
    return {
        "group_a": group_a,
        "group_b": group_b,
        "max_cuts": result.fval,
        "status": "optimized"
    }

# --- TEST LOCAL ---
if __name__ == "__main__":
    test_edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    print(solve_logistics_problem(test_edges))