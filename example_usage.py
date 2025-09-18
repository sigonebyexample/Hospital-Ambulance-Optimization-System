#!/usr/bin/env python3
"""
Example usage of the hospital optimization package.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graphical_hospital_optimization import GraphicalHospitalOptimization
from graphical_hill_climbing import GraphicalHillClimbingOptimizer

def main():
    print("Hospital Optimization Example")
    print("=" * 40)
    
    problem = GraphicalHospitalOptimization(
        grid_width=10,
        grid_height=10,
        num_houses=8,
        num_ambulances=2,
        num_hospitals=1
    )
    
    print(f"Initial cost: {problem.total_cost():.2f}")
    
    optimizer = GraphicalHillClimbingOptimizer(
        max_iterations=500,
        max_no_improvement=50
    )
    
    result = optimizer.optimize(problem)
    print(f"Final cost: {result.total_cost():.2f}")
    print(f"Improvement: {problem.total_cost() - result.total_cost():.2f}")

if __name__ == "__main__":
    main()
