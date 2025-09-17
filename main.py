import random
from typing import List, Tuple
from image_utils import ImageLoader

class Hospital:
    def __init__(self):
        self.positives: List[Tuple[int, int]] = []
        self.image_loader = ImageLoader()
    
    @classmethod
    def get_cost(cls, positions: List[Tuple[int, int]]) -> int:
        distance_threshold = 1
        
        cost = 0
        for (x, y) in positions:
            if x >= len(Space.instance.widths):
                continue
            
            current_cost = 0
            for pos in Space.instance.current_positions:
                if pos[1] == y and abs(pos[0] - x) <= distance_threshold:
                    current_cost += 1
        
        return cost

class Ambulance:
    def __init__(self):
        self.positives: List[Tuple[int, int]] = []
        self.image_loader = ImageLoader()
    
    @classmethod
    def get_cost(cls, positions: List[Tuple[int, int]]) -> int:
        current_cost = 0
        for (x, y) in positions:
            if x >= len(Space.instance.widths):
                continue
            current_cost += 1
        return current_cost

class Space:
    instance = None
    
    def __init__(self, width: int, height: int, num_houses: int = 0, num_ambulances: int = 0):
        Space.instance = self
        self.widths = width
        self.height = height
        self.num_houses = num_houses
        self._num_ambulances = num_ambulances
        self.current_positions: List[Tuple[int, int]] = []
        self.houses: List[Tuple[int, int]] = []
        self.ambulances: List[Tuple[int, int]] = []
        self.image_loader = ImageLoader()
        
    def load_images(self):
        """Load and verify all required images"""
        return self.image_loader.load_images()

    def remove_house(self, pos: Tuple[int, int]):
        if pos in self.current_positions:
            self.current_positions.remove(pos)
        if pos in self.houses:
            self.houses.remove(pos)

    def remove_ambulance(self, pos: Tuple[int, int]):
        if pos in self.current_positions:
            self.current_positions.remove(pos)
        if pos in self.ambulances:
            self.ambulances.remove(pos)

    def get_cost_dict(self, positions: List[Tuple[int, int]]):
        cost_dict = {}
        
        for (x, y) in positions:
            house_cost = 100 if (x, y) in self.houses else 0
            ambulance_cost = 100 if (x, y) in self.ambulances else 0
            
            if house_cost + ambulance_cost > 0:
                distance_threshold = 4
            else:
                distance_threshold = float('inf')
            
            total = 1 + distance_threshold * 2
            cost_dict[(x, y)] = total
        
        return cost_dict

    def __str__(self):
        return f"Houses: {len(self.houses)}, Ambulances: {len(self.ambulances)}"

    @property
    def num_ambulances(self):
        return len(self.ambulances)

    @num_ambulances.setter
    def num_ambulances(self, value: int) -> None:
        self._num_ambulances = value

def main():
    space = Space(25, 5, 10)
    
    # Load and verify images
    print("\nLoading images...")
    images = space.load_images()
    
    print("\nCurrent State:")
    print(f"Houses: {len(space.houses)}")
    print(f"Ambulances: {space.num_ambulances}")
    print(f"Space: {space}")
    print(f"Available images: {list(images.keys())}")

if __name__ == "__main__":
    main()
