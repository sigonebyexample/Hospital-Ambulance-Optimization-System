import random
import math
import cv2
import numpy as np
from typing import List, Tuple, Dict
import os

class GraphicalHospitalOptimization:
    def __init__(self, grid_width: int = 15, grid_height: int = 15, 
                 num_houses: int = 20, num_ambulances: int = 4, 
                 num_hospitals: int = 3):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.num_houses = num_houses
        self.num_ambulances = num_ambulances
        self.num_hospitals = num_hospitals
        
        # Initialize positions
        self.houses = self._generate_random_positions(num_houses)
        self.ambulances = self._generate_random_positions(num_ambulances)
        self.hospitals = self._generate_random_positions(num_hospitals)
        
        # Cost weights
        self.house_hospital_weight = 1.0
        self.ambulance_hospital_weight = 2.0
        self.ambulance_house_weight = 1.5
        
        # Load images
        self.house_img = self._load_image("../images/house.jpg", (50, 50))
        self.ambulance_img = self._load_image("../images/ambulance.jpg", (50, 50))
        self.hospital_img = self._load_image("../images/hospital.jpg", (50, 50))
        
        # Create hospital image if not exists
        if self.hospital_img is None:
            self.hospital_img = self._create_hospital_image((50, 50))
    
    def _load_image(self, image_path: str, size: Tuple[int, int]):
        """Load and resize an image"""
        if os.path.exists(image_path):
            img = cv2.imread(image_path)
            if img is not None:
                img = cv2.resize(img, size)
                return img
        print(f"Warning: Image {image_path} not found, using generated image")
        return None
    
    def _create_hospital_image(self, size: Tuple[int, int]):
        """Create a hospital image programmatically"""
        img = np.ones((size[1], size[0], 3), dtype=np.uint8) * 255
        
        # Draw red cross
        center_x, center_y = size[0] // 2, size[1] // 2
        cross_size = 15
        thickness = 3
        
        cv2.line(img, (center_x, center_y - cross_size), 
                (center_x, center_y + cross_size), (0, 0, 255), thickness)
        cv2.line(img, (center_x - cross_size, center_y), 
                (center_x + cross_size, center_y), (0, 0, 255), thickness)
        
        cv2.rectangle(img, (10, 20), (40, 45), (255, 0, 0), 2)
        return img
    
    def _generate_random_positions(self, count: int) -> List[Tuple[int, int]]:
        """Generate random positions on the grid"""
        positions = []
        for _ in range(count):
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            positions.append((x, y))
        return positions
    
    def euclidean_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calculate Euclidean distance between two positions"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def total_cost(self) -> float:
        """Calculate total cost of current configuration"""
        total = 0.0
        
        for house in self.houses:
            min_dist = min(self.euclidean_distance(house, hospital) 
                         for hospital in self.hospitals)
            total += min_dist * self.house_hospital_weight
        
        for ambulance in self.ambulances:
            min_dist = min(self.euclidean_distance(ambulance, hospital) 
                         for hospital in self.hospitals)
            total += min_dist * self.ambulance_hospital_weight
        
        for house in self.houses:
            min_ambulance_dist = min(self.euclidean_distance(house, ambulance) 
                                   for ambulance in self.ambulances)
            total += min_ambulance_dist * self.ambulance_house_weight
        
        return total
    
    def get_neighbor(self) -> 'GraphicalHospitalOptimization':
        """Generate a neighbor solution by moving one entity"""
        neighbor = self.copy()
        
        entity_type = random.choice(['hospital', 'ambulance'])
        
        if entity_type == 'hospital' and self.hospitals:
            idx = random.randint(0, len(self.hospitals) - 1)
            old_pos = neighbor.hospitals[idx]
            new_pos = self._get_valid_neighbor_position(old_pos)
            neighbor.hospitals[idx] = new_pos
            
        elif entity_type == 'ambulance' and self.ambulances:
            idx = random.randint(0, len(self.ambulances) - 1)
            old_pos = neighbor.ambulances[idx]
            new_pos = self._get_valid_neighbor_position(old_pos)
            neighbor.ambulances[idx] = new_pos
            
        return neighbor
    
    def _get_valid_neighbor_position(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Get a valid neighboring position"""
        x, y = pos
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        valid_moves = []
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height):
                valid_moves.append((new_x, new_y))
        
        return random.choice(valid_moves) if valid_moves else pos
    
    def copy(self) -> 'GraphicalHospitalOptimization':
        """Create a copy of the current state"""
        new_state = GraphicalHospitalOptimization(self.grid_width, self.grid_height,
                                                self.num_houses, self.num_ambulances,
                                                self.num_hospitals)
        new_state.houses = self.houses.copy()
        new_state.ambulances = self.ambulances.copy()
        new_state.hospitals = self.hospitals.copy()
        return new_state
    
    def create_visualization(self, show_paths: bool = False) -> np.ndarray:
        """Create a graphical visualization of the grid"""
        cell_size = 60
        padding = 20
        legend_height = 100
        
        grid_width_px = self.grid_width * cell_size + 2 * padding
        grid_height_px = self.grid_height * cell_size + 2 * padding + legend_height
        grid_img = np.ones((grid_height_px, grid_width_px, 3), dtype=np.uint8) * 240
        
        for i in range(self.grid_width + 1):
            x = padding + i * cell_size
            cv2.line(grid_img, (x, padding), (x, padding + self.grid_height * cell_size), (200, 200, 200), 1)
        
        for i in range(self.grid_height + 1):
            y = padding + i * cell_size
            cv2.line(grid_img, (padding, y), (padding + self.grid_width * cell_size, y), (200, 200, 200), 1)
        
        for x, y in self.houses:
            img_x = padding + x * cell_size + (cell_size - 50) // 2
            img_y = padding + y * cell_size + (cell_size - 50) // 2
            if self.house_img is not None:
                grid_img[img_y:img_y+50, img_x:img_x+50] = self.house_img
            else:
                cv2.rectangle(grid_img, (img_x, img_y), (img_x+50, img_y+50), (0, 255, 0), -1)
        
        for x, y in self.ambulances:
            img_x = padding + x * cell_size + (cell_size - 50) // 2
            img_y = padding + y * cell_size + (cell_size - 50) // 2
            if self.ambulance_img is not None:
                grid_img[img_y:img_y+50, img_x:img_x+50] = self.ambulance_img
            else:
                cv2.rectangle(grid_img, (img_x, img_y), (img_x+50, img_y+50), (255, 0, 0), -1)
        
        for x, y in self.hospitals:
            img_x = padding + x * cell_size + (cell_size - 50) // 2
            img_y = padding + y * cell_size + (cell_size - 50) // 2
            if self.hospital_img is not None:
                grid_img[img_y:img_y+50, img_x:img_x+50] = self.hospital_img
            else:
                cv2.rectangle(grid_img, (img_x, img_y), (img_x+50, img_y+50), (0, 0, 255), -1)
        
        if show_paths:
            self._draw_paths(grid_img, padding, cell_size)
        
        legend_y = padding + self.grid_height * cell_size + 10
        self._draw_legend(grid_img, legend_y, padding, cell_size)
        
        cost_text = f"Total Cost: {self.total_cost():.2f}"
        cv2.putText(grid_img, cost_text, (padding, legend_y + 80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        return grid_img
    
    def _draw_paths(self, grid_img: np.ndarray, padding: int, cell_size: int):
        for house in self.houses:
            nearest_hospital = min(self.hospitals, key=lambda h: self.euclidean_distance(house, h))
            self._draw_line(grid_img, house, nearest_hospital, padding, cell_size, (0, 255, 0), 1)
        
        for ambulance in self.ambulances:
            nearest_hospital = min(self.hospitals, key=lambda h: self.euclidean_distance(ambulance, h))
            self._draw_line(grid_img, ambulance, nearest_hospital, padding, cell_size, (255, 0, 0), 1)
    
    def _draw_line(self, grid_img: np.ndarray, pos1: Tuple[int, int], pos2: Tuple[int, int], 
                  padding: int, cell_size: int, color: Tuple[int, int, int], thickness: int):
        x1 = padding + pos1[0] * cell_size + cell_size // 2
        y1 = padding + pos1[1] * cell_size + cell_size // 2
        x2 = padding + pos2[0] * cell_size + cell_size // 2
        y2 = padding + pos2[1] * cell_size + cell_size // 2
        cv2.line(grid_img, (x1, y1), (x2, y2), color, thickness)
    
    def _draw_legend(self, grid_img: np.ndarray, legend_y: int, padding: int, cell_size: int):
        if self.house_img is not None:
            grid_img[legend_y:legend_y+30, padding:padding+30] = cv2.resize(self.house_img, (30, 30))
        else:
            cv2.rectangle(grid_img, (padding, legend_y), (padding+30, legend_y+30), (0, 255, 0), -1)
        cv2.putText(grid_img, "House", (padding+40, legend_y+20), cv2.FONT_HERSHEY_SIMPLEX, 
                  0.5, (0, 0, 0), 1)
        
        if self.ambulance_img is not None:
            grid_img[legend_y:legend_y+30, padding+120:padding+150] = cv2.resize(self.ambulance_img, (30, 30))
        else:
            cv2.rectangle(grid_img, (padding+120, legend_y), (padding+150, legend_y+30), (255, 0, 0), -1)
        cv2.putText(grid_img, "Ambulance", (padding+160, legend_y+20), cv2.FONT_HERSHEY_SIMPLEX, 
                  0.5, (0, 0, 0), 1)
        
        if self.hospital_img is not None:
            grid_img[legend_y:legend_y+30, padding+250:padding+280] = cv2.resize(self.hospital_img, (30, 30))
        else:
            cv2.rectangle(grid_img, (padding+250, legend_y), (padding+280, legend_y+30), (0, 0, 255), -1)
        cv2.putText(grid_img, "Hospital", (padding+290, legend_y+20), cv2.FONT_HERSHEY_SIMPLEX, 
                  0.5, (0, 0, 0), 1)
    
    def display(self, window_name: str = "Hospital Optimization", show_paths: bool = False):
        visualization = self.create_visualization(show_paths)
        cv2.imshow(window_name, visualization)
        cv2.waitKey(1)
    
    def save_visualization(self, filename: str, show_paths: bool = False):
        visualization = self.create_visualization(show_paths)
        cv2.imwrite(filename, visualization)
