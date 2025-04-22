# Database Integration Guide for Agri-Vision System

This guide provides instructions for integrating a database with the Agri-Vision System to store and retrieve persistent data for the application.

## Database Options

### PostgreSQL (Recommended)

PostgreSQL is recommended for the Agri-Vision System due to its robust geospatial capabilities through the PostGIS extension, which is ideal for storing farm field boundaries, coordinates, and other geospatial data.

### SQLite (Lightweight Option)

For simpler deployments or testing purposes, SQLite can be used as a lightweight alternative to PostgreSQL.

## Database Schema

The following tables are recommended for the Agri-Vision System:

### 1. Farms

```sql
CREATE TABLE farms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    total_area FLOAT,
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Fields

```sql
CREATE TABLE fields (
    id SERIAL PRIMARY KEY,
    farm_id INTEGER REFERENCES farms(id),
    name VARCHAR(100) NOT NULL,
    area FLOAT,
    crop_type VARCHAR(50),
    boundaries JSON, -- Store GeoJSON format field boundaries
    planting_date DATE,
    expected_harvest_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3. Crop Health Data

```sql
CREATE TABLE crop_health (
    id SERIAL PRIMARY KEY,
    field_id INTEGER REFERENCES fields(id),
    date DATE NOT NULL,
    ndvi_avg FLOAT,
    ndvi_min FLOAT,
    ndvi_max FLOAT,
    health_index INTEGER, -- 0-100 scale
    image_url VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Weather Data

```sql
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    farm_id INTEGER REFERENCES farms(id),
    date DATE NOT NULL,
    temperature_max FLOAT,
    temperature_min FLOAT,
    temperature_avg FLOAT,
    humidity_avg FLOAT,
    precipitation FLOAT,
    wind_speed FLOAT,
    conditions VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Yield Data

```sql
CREATE TABLE yield_data (
    id SERIAL PRIMARY KEY,
    field_id INTEGER REFERENCES fields(id),
    season VARCHAR(50),
    year INTEGER,
    yield_amount FLOAT,
    yield_unit VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 6. Resource Usage

```sql
CREATE TABLE resource_usage (
    id SERIAL PRIMARY KEY,
    field_id INTEGER REFERENCES fields(id),
    date DATE NOT NULL,
    resource_type VARCHAR(20), -- 'water', 'fertilizer', 'pesticide', etc.
    amount FLOAT,
    unit VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Integration Steps

### 1. Install Required Packages

```bash
pip install sqlalchemy psycopg2-binary python-dotenv
```

### 2. Configure Database Connection

Create a `.env` file with database connection parameters:

```
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=agrivision
```

### 3. Create Database Connection Module

Create a file `utils/database.py`:

```python
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4. Create Database Models

Create a file `utils/models.py`:

```python
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, JSON, TIMESTAMP, func
from sqlalchemy.orm import relationship
from utils.database import Base

class Farm(Base):
    __tablename__ = "farms"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100))
    total_area = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    fields = relationship("Field", back_populates="farm")
    weather_data = relationship("WeatherData", back_populates="farm")

class Field(Base):
    __tablename__ = "fields"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    name = Column(String(100), nullable=False)
    area = Column(Float)
    crop_type = Column(String(50))
    boundaries = Column(JSON)
    planting_date = Column(Date)
    expected_harvest_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    farm = relationship("Farm", back_populates="fields")
    crop_health = relationship("CropHealth", back_populates="field")
    yield_data = relationship("YieldData", back_populates="field")
    resource_usage = relationship("ResourceUsage", back_populates="field")

class CropHealth(Base):
    __tablename__ = "crop_health"
    
    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"))
    date = Column(Date, nullable=False)
    ndvi_avg = Column(Float)
    ndvi_min = Column(Float)
    ndvi_max = Column(Float)
    health_index = Column(Integer)
    image_url = Column(String(255))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    field = relationship("Field", back_populates="crop_health")

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    date = Column(Date, nullable=False)
    temperature_max = Column(Float)
    temperature_min = Column(Float)
    temperature_avg = Column(Float)
    humidity_avg = Column(Float)
    precipitation = Column(Float)
    wind_speed = Column(Float)
    conditions = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    farm = relationship("Farm", back_populates="weather_data")

class YieldData(Base):
    __tablename__ = "yield_data"
    
    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"))
    season = Column(String(50))
    year = Column(Integer)
    yield_amount = Column(Float)
    yield_unit = Column(String(20))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    field = relationship("Field", back_populates="yield_data")

class ResourceUsage(Base):
    __tablename__ = "resource_usage"
    
    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"))
    date = Column(Date, nullable=False)
    resource_type = Column(String(20))
    amount = Column(Float)
    unit = Column(String(20))
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    field = relationship("Field", back_populates="resource_usage")
```

### 5. Create Database Initialization Script

Create a file `utils/init_db.py`:

```python
from utils.database import engine, Base
from utils.models import Farm, Field, CropHealth, WeatherData, YieldData, ResourceUsage

def init_database():
    """Initialize the database by creating all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")

if __name__ == "__main__":
    init_database()
```

### 6. Create Data Access Layer

Create a file `utils/data_access.py`:

```python
from sqlalchemy.orm import Session
from utils.models import Farm, Field, CropHealth, WeatherData, YieldData, ResourceUsage
from datetime import datetime, date
from typing import List, Dict, Any, Optional

# Farm operations
def create_farm(db: Session, farm_data: Dict[str, Any]) -> Farm:
    farm = Farm(**farm_data)
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm

def get_farm(db: Session, farm_id: int) -> Optional[Farm]:
    return db.query(Farm).filter(Farm.id == farm_id).first()

def get_farms(db: Session, skip: int = 0, limit: int = 100) -> List[Farm]:
    return db.query(Farm).offset(skip).limit(limit).all()

# Field operations
def create_field(db: Session, field_data: Dict[str, Any]) -> Field:
    field = Field(**field_data)
    db.add(field)
    db.commit()
    db.refresh(field)
    return field

def get_field(db: Session, field_id: int) -> Optional[Field]:
    return db.query(Field).filter(Field.id == field_id).first()

def get_fields_by_farm(db: Session, farm_id: int) -> List[Field]:
    return db.query(Field).filter(Field.farm_id == farm_id).all()

# Crop health operations
def create_crop_health(db: Session, crop_health_data: Dict[str, Any]) -> CropHealth:
    crop_health = CropHealth(**crop_health_data)
    db.add(crop_health)
    db.commit()
    db.refresh(crop_health)
    return crop_health

def get_crop_health_by_field(db: Session, field_id: int) -> List[CropHealth]:
    return db.query(CropHealth).filter(CropHealth.field_id == field_id).all()

def get_crop_health_by_date_range(db: Session, field_id: int, start_date: date, end_date: date) -> List[CropHealth]:
    return db.query(CropHealth).filter(
        CropHealth.field_id == field_id,
        CropHealth.date >= start_date,
        CropHealth.date <= end_date
    ).all()

# Weather data operations
def create_weather_data(db: Session, weather_data: Dict[str, Any]) -> WeatherData:
    weather = WeatherData(**weather_data)
    db.add(weather)
    db.commit()
    db.refresh(weather)
    return weather

def get_weather_data_by_farm(db: Session, farm_id: int, start_date: date, end_date: date) -> List[WeatherData]:
    return db.query(WeatherData).filter(
        WeatherData.farm_id == farm_id,
        WeatherData.date >= start_date,
        WeatherData.date <= end_date
    ).all()

# Yield data operations
def create_yield_data(db: Session, yield_data: Dict[str, Any]) -> YieldData:
    yield_entry = YieldData(**yield_data)
    db.add(yield_entry)
    db.commit()
    db.refresh(yield_entry)
    return yield_entry

def get_yield_data_by_field(db: Session, field_id: int) -> List[YieldData]:
    return db.query(YieldData).filter(YieldData.field_id == field_id).all()

# Resource usage operations
def create_resource_usage(db: Session, resource_data: Dict[str, Any]) -> ResourceUsage:
    resource = ResourceUsage(**resource_data)
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource

def get_resource_usage_by_field(db: Session, field_id: int, resource_type: Optional[str] = None) -> List[ResourceUsage]:
    query = db.query(ResourceUsage).filter(ResourceUsage.field_id == field_id)
    if resource_type:
        query = query.filter(ResourceUsage.resource_type == resource_type)
    return query.all()
```

### 7. Modify Data Processor to Use Database

Update `utils/data_processor.py` to use the database:

```python
# Add at the beginning of the file
from utils.database import get_db
from utils.data_access import (
    get_farms, get_fields_by_farm, get_crop_health_by_field,
    get_weather_data_by_farm, get_yield_data_by_field, get_resource_usage_by_field
)
from datetime import datetime, timedelta

# Modify load_sample_data to use database data when available
def load_sample_data(data_type):
    """
    Load data from the database or fall back to sample data if database not available
    
    Parameters:
    data_type (str): Type of data to load ('crop_data', 'weather_data', 'soil_data', etc.)
    
    Returns:
    DataFrame: Pandas DataFrame containing the requested data
    """
    try:
        # Try to get a database session
        db = next(get_db())
        
        if data_type == "farms":
            farms = get_farms(db)
            # Convert to DataFrame...
            
        elif data_type == "fields":
            farm_id = 1  # Default farm ID, replace with actual selected farm
            fields = get_fields_by_farm(db, farm_id)
            # Convert to DataFrame...
            
        elif data_type == "crop_health":
            field_id = 1  # Default field ID, replace with actual selected field
            crop_health = get_crop_health_by_field(db, field_id)
            # Convert to DataFrame...
            
        # Add more cases for other data types...
        
        # If data retrieval was successful, return the data
        return df
        
    except Exception as e:
        print(f"Database error: {e}")
        
        # Fall back to sample data (existing implementation)
        # ... (existing code to generate sample data)
```

### 8. Database Migration Script

Create a file `utils/migrate_db.py` for database migrations:

```python
import os
from alembic import command
from alembic.config import Config

def run_migrations():
    """Run database migrations using Alembic"""
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "..", "alembic.ini"))
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()
```

## Using the Database in Streamlit Pages

Update the Streamlit pages to use the database:

```python
# At the beginning of each page file
from utils.database import get_db
from utils.data_access import get_farms, get_fields_by_farm  # Import relevant functions

# Then in the page content
def render_page():
    # Get data from database
    db = next(get_db())
    farms = get_farms(db)
    
    # Use the data in Streamlit components
    farm_names = [farm.name for farm in farms]
    selected_farm = st.selectbox("Select Farm", farm_names)
    
    # Get the selected farm ID
    selected_farm_id = next((farm.id for farm in farms if farm.name == selected_farm), None)
    
    # Get fields for the selected farm
    if selected_farm_id:
        fields = get_fields_by_farm(db, selected_farm_id)
        # Use fields data...
```

## Converting from Sample Data to Database Data

To transition from sample data to real database data:

1. Create a data import script that can read from CSV/Excel files
2. Create a database admin page in Streamlit for data entry
3. Implement batch data import for historical data

## PostGIS Integration

For enhanced geospatial capabilities:

1. Install PostGIS extension in PostgreSQL
2. Modify the Field model to use PostGIS geometry types
3. Use PostGIS functions for spatial queries and analysis

## Performance Considerations

1. Add indexes for frequently queried columns
2. Use database connection pooling for production
3. Implement caching for frequently accessed data
4. Consider materialized views for complex aggregations