import random
import cv2
from graphical_hospital_optimization import GraphicalHospitalOptimization
from graphical_hill_climbing import GraphicalHillClimbingOptimizer, SimulatedAnnealingOptimizer

def main():
    random.seed(42)
    
    print("Creating graphical hospital optimization problem...")
    problem = GraphicalHospitalOptimization(
        grid_width=12,
        grid_height=12,
        num_houses=15,
        num_ambulances=3,
        num_hospitals=2
    )
    
    print("\nInitial configuration:")
    initial_cost = problem.total_cost()
    print(f"Initial total cost: {initial_cost:.2f}")
    
    problem.display("Initial State")
    problem.save_visualization("../results/initial_state.jpg")
    print("Initial state saved as '../results/initial_state.jpg'")
    
    print("\nRunning Hill Climbing optimization with graphical display...")
    print("Press any key on the image windows to continue...")
    
    optimizer = GraphicalHillClimbingOptimizer(
        max_iterations=2000, 
        max_no_improvement=200,
        display_frequency=20
    )
    
    optimized_solution = optimizer.optimize(problem)
    
    print("\nOptimization completed!")
    final_cost = optimized_solution.total_cost()
    print(f"Final total cost: {final_cost:.2f}")
    print(f"Cost improvement: {initial_cost - final_cost:.2f}")
    print(f"Improvement percentage: {(initial_cost - final_cost) / initial_cost * 100:.1f}%")
    
    print("\nPress any key to close all windows...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
