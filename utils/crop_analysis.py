import numpy as np
import random
from PIL import Image
import io

def analyze_crop_image(image_file):
    """
    Analyze crop image for disease detection.
    This is a simulation function that would normally use computer vision and AI models.
    
    Parameters:
    image_file: Image file uploaded by user
    
    Returns:
    dict: Analysis results
    """
    # In a real application, this would use computer vision and machine learning
    # to analyze the image. For demonstration, we'll return simulated results.
    
    # Read image file
    try:
        image = Image.open(image_file)
        # Basic image validation
        if image.width < 50 or image.height < 50:
            return {
                "success": False,
                "error": "Image too small for analysis"
            }
            
        # Randomly determine if a disease is detected (for demo purposes)
        disease_detected = random.choice([True, False])
        
        if disease_detected:
            # Randomly select a disease
            diseases = [
                {
                    "name": "Wheat Leaf Rust",
                    "confidence": random.randint(80, 95),
                    "description": "Orange-brown pustules on leaves that reduce photosynthesis and yield. Control with fungicides and resistant varieties."
                },
                {
                    "name": "Rice Blast",
                    "confidence": random.randint(85, 98),
                    "description": "Diamond-shaped lesions on leaves. Can kill plants at seedling stage. Manage with fungicides and resistant varieties."
                },
                {
                    "name": "Cotton Leaf Curl Virus",
                    "confidence": random.randint(75, 90),
                    "description": "Upward curling of leaves with thickened veins. Spread by whiteflies. Use resistant varieties and control insect vectors."
                },
                {
                    "name": "Sugarcane Red Rot",
                    "confidence": random.randint(80, 92),
                    "description": "Red discoloration inside stalks. Causes withering and death. Use disease-free seed cane and resistant varieties."
                }
            ]
            selected_disease = random.choice(diseases)
            
            return {
                "success": True,
                "disease_detected": True,
                "disease_name": selected_disease["name"],
                "confidence": selected_disease["confidence"],
                "description": selected_disease["description"],
                "image_size": f"{image.width}x{image.height}"
            }
        else:
            return {
                "success": True,
                "disease_detected": False,
                "confidence": random.randint(85, 98),
                "image_size": f"{image.width}x{image.height}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error analyzing image: {str(e)}"
        }

def get_crop_health_metrics(field_name, crop_type):
    """
    Get health metrics for a specific field and crop.
    
    Parameters:
    field_name (str): Name of the field
    crop_type (str): Type of crop
    
    Returns:
    dict: Health metrics
    """
    # In a real app, this would retrieve data from sensors, drones, or satellites
    # For demonstration, we'll return simulated results
    
    # Base values based on crop type
    if crop_type == "Wheat":
        base_ndvi = 0.82
        base_stress = 12
        base_moisture = 28
    elif crop_type == "Rice":
        base_ndvi = 0.78
        base_stress = 15
        base_moisture = 35
    elif crop_type == "Cotton":
        base_ndvi = 0.75
        base_stress = 18
        base_moisture = 25
    else:
        base_ndvi = 0.80
        base_stress = 14
        base_moisture = 30
    
    # Add some variation
    ndvi = max(0, min(1, base_ndvi + np.random.normal(0, 0.05)))
    stress = max(0, base_stress + np.random.normal(0, 3))
    moisture = max(0, base_moisture + np.random.normal(0, 5))
    
    # Calculate health score (0-100) based on NDVI and stress
    health_score = int(min(100, max(0, ndvi * 100 - stress)))
    
    # Determine risk level based on health score
    if health_score >= 80:
        risk_level = "Low"
    elif health_score >= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    return {
        "field_name": field_name,
        "crop_type": crop_type,
        "ndvi": round(ndvi, 2),
        "stress_index": round(stress, 1),
        "moisture": round(moisture, 1),
        "health_score": health_score,
        "risk_level": risk_level,
        "timestamp": str(np.datetime64('now'))
    }