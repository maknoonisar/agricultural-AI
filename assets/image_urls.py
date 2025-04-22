import random

# Dictionary of image URLs for different categories
image_urls = {
    "farming_landscapes_pakistan": [
        "https://images.pexels.com/photos/4207909/pexels-photo-4207909.jpeg",
        "https://images.pexels.com/photos/4555468/pexels-photo-4555468.jpeg",
        "https://images.pexels.com/photos/4555467/pexels-photo-4555467.jpeg",
        "https://images.pexels.com/photos/4262424/pexels-photo-4262424.jpeg",
        "https://images.pexels.com/photos/2397652/pexels-photo-2397652.jpeg"
    ],
    "modern_agriculture_technology": [
        "https://images.pexels.com/photos/2132250/pexels-photo-2132250.jpeg",
        "https://images.pexels.com/photos/2437291/pexels-photo-2437291.jpeg",
        "https://images.pexels.com/photos/4503470/pexels-photo-4503470.jpeg",
        "https://images.pexels.com/photos/2223082/pexels-photo-2223082.jpeg",
        "https://images.pexels.com/photos/1112080/pexels-photo-1112080.jpeg"
    ],
    "crop_disease_examples": [
        "https://upload.wikimedia.org/wikipedia/commons/7/76/Wheat_leaf_rust.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/6/6e/Rice_blast.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/b/b0/Cotton_leaf_curl_virus.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c5/Potato_blight.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/15/Tomato_leaf_curl.jpg"
    ]
}

def get_random_image(category):
    """
    Returns a random image URL from the specified category.
    
    Parameters:
    category (str): Category of image to retrieve
    
    Returns:
    str: URL of a random image from the category
    """
    if category in image_urls:
        return random.choice(image_urls[category])
    else:
        # Return a default image if category not found
        return "https://images.pexels.com/photos/2397652/pexels-photo-2397652.jpeg"

def get_crop_disease_images():
    """
    Returns a dictionary of crop disease images.
    
    Returns:
    dict: Dictionary with disease names as keys and image URLs as values
    """
    return {
        "Wheat Leaf Rust": "https://upload.wikimedia.org/wikipedia/commons/7/76/Wheat_leaf_rust.jpg",
        "Rice Blast": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Rice_blast.jpg",
        "Cotton Leaf Curl Virus": "https://upload.wikimedia.org/wikipedia/commons/b/b0/Cotton_leaf_curl_virus.jpg",
        "Sugarcane Red Rot": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Sugarcane_red_rot.jpg/800px-Sugarcane_red_rot.jpg",
        "Potato Late Blight": "https://upload.wikimedia.org/wikipedia/commons/c/c5/Potato_blight.jpg",
        "Tomato Yellow Leaf Curl Virus": "https://upload.wikimedia.org/wikipedia/commons/1/15/Tomato_leaf_curl.jpg"
    }