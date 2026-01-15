from qiskit_ibm_runtime import QiskitRuntimeService

# PASTE YOUR KEY INSIDE THE QUOTES BELOW
MY_TOKEN = "84wbHDtov6gzwT6JGHHsQGkTAWvFjn42y74CJttYKkvZ"

try:
    # UPDATED: We use 'ibm_quantum_platform' as the channel name
    QiskitRuntimeService.save_account(
        channel="ibm_quantum_platform", 
        token=MY_TOKEN, 
        overwrite=True,
        set_as_default=True
    )
    print("SUCCESS: Your Quantum Passport is saved.")
except Exception as e:
    print(f"Error: {e}")