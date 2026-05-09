import json
import random
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import College

def seed_data():
    db = SessionLocal()
    with open('colleges_data.json', 'r') as f:
        raw_data = json.load(f)

    for item in raw_data:
        # Map NIRF names to our DB columns
        new_college = College(
            name=item.get("Name"),
            location=f"{item.get('City')}, {item.get('State')}",
            # Generating realistic mock data for missing fields
            fees=random.randint(50000, 400000), 
            placement_rate=round(random.uniform(70, 98), 2),
            rating=round(random.uniform(3.5, 5.0), 1)
        )
        db.add(new_college)
    
    db.commit()
    print("🚀 Real data with realistic metrics injected successfully!")

if __name__ == "__main__":
    seed_data()