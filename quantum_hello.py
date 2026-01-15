from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

# 1. Build the Circuit (The "Chip" Logic)
# We create a circuit with 1 qubit and 1 classical bit to store the result.
circuit = QuantumCircuit(1, 1)

# Apply a Hadamard Gate (H-gate). 
# This puts the qubit in "Superposition" (state of being 0 and 1 at the same time).
circuit.h(0)

# Measure the qubit. 
# This forces nature to choose 0 or 1. It is TRULY random physics, not math.
circuit.measure(0, 0)

print("Quantum Circuit Created!")
print(circuit)

# 2. The Simulation (Testing it locally)
# In a real product, you'd send this to IBM's cloud. For now, we simulate it.
from qiskit.primitives import StatevectorSampler

# Run the circuit 1000 times
sampler = StatevectorSampler()
job = sampler.run([circuit], shots=1000)
result = job.result()

# Get counts (How many 0s? How many 1s?)
# Since it's truly random, it should be roughly 50/50.
counts = result[0].data.c.get_counts()
print(f"\nResult: {counts}")