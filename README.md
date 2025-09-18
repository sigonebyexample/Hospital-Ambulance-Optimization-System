# Hospital Optimization with Hill Climbing

A graphical optimization system that uses hill climbing algorithm to optimally place hospitals and ambulances to minimize transportation costs.

## Features

- 🏥 Graphical visualization using OpenCV
- 🚑 Real image display for houses, ambulances, and hospitals
- 📊 Cost minimization for hospital and ambulance placement
- 🔄 Hill climbing optimization algorithm
- 💾 Image saving capabilities
- 📈 Real-time progress visualization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sigonebyexample/hospital-optimization.git
cd hospital-optimization
```
## Usage
```bash
python src/main_graphical_optimization.py
```
## Requirements
``` bash
pip install -r src/requirements.txt
    
```
## Or use the module:
``` bash
#make python file and run this code 
from src.graphical_hospital_optimization import GraphicalHospitalOptimization
from src.graphical_hill_climbing import GraphicalHillClimbingOptimizer

problem = GraphicalHospitalOptimization(
    grid_width=12,
    grid_height=12,
    num_houses=15,
    num_ambulances=3,
    num_hospitals=2
)

optimizer = GraphicalHillClimbingOptimizer()
result = optimizer.optimize(problem)
```
## Project Structure
``` bash
hospital-optimization/
├── images/          # Image assets
├── src/            # Source code
├── results/        # Output images
├── examples/       # Usage examples
├── tests/          # Unit tests
└── README.md       # This file
```
