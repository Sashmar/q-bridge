import os
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

def get_quantum_randomness():
    print("1. Authenticating with IBM Cloud...")
    
    # CLOUD FIX: Try to get key from Environment (Render), otherwise use Local (Laptop)
    my_token = os.getenv("IBM_QUANTUM_TOKEN")
    
    try:
        if my_token:
            # We are on the Cloud (Render)
            service = QiskitRuntimeService(channel="ibm_quantum_platform", token=my_token)
        else:
            # We are on Local Laptop (uses saved_account)
            service = QiskitRuntimeService()
    except Exception as e:
        return {"error": "Authentication Failed. Check API Key.", "details": str(e)}
    
    # FIND THE REAL HARDWARE
    print("2. Finding the fastest available Quantum Computer...")
    try:
        backend = service.least_busy(operational=True, simulator=False)
        print(f"   > Found: {backend.name}")
    except:
        # Fallback if no real hardware is available immediately
        print("   > All real chips busy, falling back to simulator for demo...")
        return {"error": "All Quantum Chips are busy. Try again in 5 mins."}
    
    # THE CIRCUIT
    qc = QuantumCircuit(1)
    qc.h(0)             
    qc.measure_all()    
    
    # TRANSPILATION
    print(f"3. Transpiling code for {backend.name}...")
    isa_circuit = transpile(qc, backend)
    
    # EXECUTE
    print(f"4. Sending job to {backend.name}...")
    sampler = Sampler(backend)
    job = sampler.run([isa_circuit])
    
    print(f"   > Job ID: {job.job_id()} (Waiting...)")
    result = job.result()
    
    # PARSE RESULT
    counts = result[0].data.meas.get_counts()
    print(f"5. Success! Quantum Data: {counts}")
    return counts

if __name__ == "__main__":
    get_quantum_randomness()