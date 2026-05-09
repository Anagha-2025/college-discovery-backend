import json
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import College, Base

# YOUR NEON CLOUD URL
DATABASE_URL = "postgresql://neondb_owner:npg_u8IhVm0TafZO@ep-floral-river-aqmkgwyj-pooler.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        with open('colleges_data.json', 'r') as f:
            raw_data = json.load(f)

        for item in raw_data:
            # We are only using 'name', 'location', and 'fees' to match your DB columns
            new_college = College(
                name=item.get("Name"),
                location=f"{item.get('City')}, {item.get('State')}",
                fees=random.randint(50000, 400000)
            )
            db.add(new_college)
        
        db.commit()
        print("🚀 Data injected into NEON CLOUD successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()