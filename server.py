from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Tuple
import os

# Import your engines
from qpu_bridge import get_quantum_randomness
from quantum_optimizer import solve_logistics_problem

app = FastAPI()

# --- INPUT MODEL ---
class LogisticsRequest(BaseModel):
    routes: List[Tuple[int, int]]

# --- API ROUTES (The Brains) ---

@app.get("/generate-quantum-number")
def quantum_endpoint():
    print(">>> Spooling up Randomness Engine...")
    data = get_quantum_randomness()
    return {
        "source": "Real Quantum Computer (IBM Cloud)",
        "raw_data": data,
        "status": "success"
    }

@app.post("/optimize-logistics")
def optimize_endpoint(request: LogisticsRequest):
    print(f">>> Optimization Request received for {len(request.routes)} routes.")
    result = solve_logistics_problem(request.routes)
    return {
        "algorithm": "QAOA (Quantum Approximate Optimization Algorithm)",
        "optimization_result": result
    }

# --- FRONTEND ROUTE (The Face) ---
# This serves your index.html when someone visits the main URL
@app.get("/")
def read_root():
    return FileResponse('index.html')

# If you had more static files (images/css), you'd mount them here.
# For now, we just need index.html.