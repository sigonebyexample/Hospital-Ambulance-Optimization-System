import os
from PIL import Image
import matplotlib.pyplot as plt

class ImageLoader:
    def __init__(self, image_folder="."):
        self.image_folder = image_folder
        self.ambulance_image = "ambulance6.jpg"
        self.house_image = "50819.jpg"
        
    def load_images(self):
        """Load and verify images exist"""
        images = {}
        
        if os.path.exists(self.ambulance_image):
            images['ambulance'] = self.ambulance_image
            print(f"Ambulance image found: {self.ambulance_image}")
        else:
            print(f"Warning: Ambulance image not found: {self.ambulance_image}")
            
        if os.path.exists(self.house_image):
            images['house'] = self.house_image
            print(f"House image found: {self.house_image}")
        else:
            print(f"Warning: House image not found: {self.house_image}")
            
        return images
    
    def display_image(self, image_path, title="Image"):
        """Display an image using matplotlib"""
        try:
            img = Image.open(image_path)
            plt.figure(figsize=(8, 6))
            plt.imshow(img)
            plt.title(title)
            plt.axis('off')
            plt.show()
            return True
        except Exception as e:
            print(f"Error displaying image {image_path}: {e}")
            return False

# Example usage
if __name__ == "__main__":
    loader = ImageLoader()
    images = loader.load_images()
    
    if 'ambulance' in images:
        loader.display_image(images['ambulance'], "Ambulance")
    
    if 'house' in images:
        loader.display_image(images['house'], "House")
