from app.core.database import Base, engine
from app.models import price_point  
from app.models import raw_market_data 
from app.models import symbol_average
from app.models import polling_job 

def init_db():
    print("Creating database tables")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully")

if __name__ == "__main__":  
    init_db()
