import cv2
import random
import math
from graphical_hospital_optimization import GraphicalHospitalOptimization

class GraphicalHillClimbingOptimizer:
    def __init__(self, max_iterations: int = 1000, max_no_improvement: int = 100,
                 display_frequency: int = 10):
        self.max_iterations = max_iterations
        self.max_no_improvement = max_no_improvement
        self.display_frequency = display_frequency
    
    def optimize(self, initial_state: GraphicalHospitalOptimization) -> GraphicalHospitalOptimization:
        current_state = initial_state
        current_cost = current_state.total_cost()
        
        best_state = current_state.copy()
        best_cost = current_cost
        
        no_improvement_count = 0
        
        print(f"Initial cost: {current_cost:.2f}")
        current_state.display("Hospital Optimization - Initial State")
        
        for iteration in range(self.max_iterations):
            if no_improvement_count >= self.max_no_improvement:
                print(f"Stopping early - no improvement for {self.max_no_improvement} iterations")
                break
            
            neighbor = current_state.get_neighbor()
            neighbor_cost = neighbor.total_cost()
            
            if neighbor_cost < current_cost:
                current_state = neighbor
                current_cost = neighbor_cost
                no_improvement_count = 0
                
                if neighbor_cost < best_cost:
                    best_state = neighbor.copy()
                    best_cost = neighbor_cost
                    print(f"Iteration {iteration}: New best cost: {best_cost:.2f}")
                    best_state.display("Hospital Optimization - Best State")
            else:
                no_improvement_count += 1
            
            if iteration % self.display_frequency == 0:
                current_state.display("Hospital Optimization - Current State")
            
            if iteration % 100 == 0:
                print(f"Iteration {iteration}: Current cost: {current_cost:.2f}")
        
        print(f"Final best cost: {best_cost:.2f}")
        print(f"Improvement: {initial_state.total_cost() - best_cost:.2f}")
        
        best_state.display("Hospital Optimization - Final Result", show_paths=True)
        best_state.save_visualization("../results/final_optimization_result.jpg", show_paths=True)
        print("Final result saved as '../results/final_optimization_result.jpg'")
        
        return best_state

class SimulatedAnnealingOptimizer:
    def __init__(self, initial_temperature: float = 1000.0, 
                 cooling_rate: float = 0.95, min_temperature: float = 0.1):
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
    
    def optimize(self, initial_state: GraphicalHospitalOptimization) -> GraphicalHospitalOptimization:
        current_state = initial_state
        current_cost = current_state.total_cost()
        
        best_state = current_state.copy()
        best_cost = current_cost
        
        temperature = self.initial_temperature
        iteration = 0
        
        print(f"Initial cost: {current_cost:.2f}")
        print(f"Initial temperature: {temperature:.2f}")
        
        while temperature > self.min_temperature:
            neighbor = current_state.get_neighbor()
            neighbor_cost = neighbor.total_cost()
            
            cost_diff = neighbor_cost - current_cost
            
            if cost_diff < 0:
                current_state = neighbor
                current_cost = neighbor_cost
                
                if neighbor_cost < best_cost:
                    best_state = neighbor.copy()
                    best_cost = neighbor_cost
                    print(f"Iteration {iteration}: New best cost: {best_cost:.2f}")
            
            else:
                acceptance_probability = math.exp(-cost_diff / temperature)
                if random.random() < acceptance_probability:
                    current_state = neighbor
                    current_cost = neighbor_cost
            
            temperature *= self.cooling_rate
            iteration += 1
            
            if iteration % 100 == 0:
                print(f"Iteration {iteration}: Cost: {current_cost:.2f}, Temp: {temperature:.2f}")
        
        print(f"Final best cost: {best_cost:.2f}")
        return best_state
