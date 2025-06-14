from app.core.database import Base, engine
from app.models import price_point  # ensures model is registered

def init_db():
    print("Creating database tables")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

if __name__ == "__main__":  # ✅ MUST be outside the function
    init_db()
