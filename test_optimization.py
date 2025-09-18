#!/usr/bin/env python3
"""
Unit tests for hospital optimization.
"""

import unittest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from graphical_hospital_optimization import GraphicalHospitalOptimization

class TestHospitalOptimization(unittest.TestCase):
    
    def setUp(self):
        self.optimization = GraphicalHospitalOptimization(
            grid_width=5,
            grid_height=5,
            num_houses=3,
            num_ambulances=1,
            num_hospitals=1
        )
    
    def test_initialization(self):
        self.assertEqual(len(self.optimization.houses), 3)
        self.assertEqual(len(self.optimization.ambulances), 1)
        self.assertEqual(len(self.optimization.hospitals), 1)
        self.assertEqual(self.optimization.grid_width, 5)
        self.assertEqual(self.optimization.grid_height, 5)
    
    def test_cost_calculation(self):
        cost = self.optimization.total_cost()
        self.assertIsInstance(cost, float)
        self.assertGreaterEqual(cost, 0)
    
    def test_neighbor_generation(self):
        neighbor = self.optimization.get_neighbor()
        self.assertIsInstance(neighbor, GraphicalHospitalOptimization)
    
    def test_copy_method(self):
        copy = self.optimization.copy()
        self.assertEqual(copy.grid_width, self.optimization.grid_width)
        self.assertEqual(copy.grid_height, self.optimization.grid_height)

if __name__ == "__main__":
    unittest.main()
