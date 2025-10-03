# db_init.py
import pandas as pd
from sqlmodel import SQLModel, create_engine, Session
from app.models import Investor, Commitment
from datetime import datetime

CSV_PATH = "data.csv"
DB_PATH = "sqlite:///investors.db"

def create_database_and_load_data():
    """Create database tables and load data from CSV"""
    engine = create_engine(DB_PATH, echo=True)
    
    # Drops all tables
    SQLModel.metadata.drop_all(engine)
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    # Load CSV data
    df = pd.read_csv(CSV_PATH)
    
    # Get unique investors and sort alphabetically for ID assignment
    investor_data = df[['Investor Name', 'Investory Type', 'Investor Country', 
                       'Investor Date Added']].drop_duplicates()
    investor_data_sorted = investor_data.sort_values('Investor Name')
    
    # Create investor mapping with alphabetical IDs
    investor_mapping = {}
    
    with Session(engine) as session:
        # Insert investors in alphabetical order
        for idx, (_, row) in enumerate(investor_data_sorted.iterrows(), 1):
            investor = Investor(
                id=idx,
                name=row['Investor Name'],
                type=row['Investory Type'],
                country=row['Investor Country'],
                date_added=datetime.strptime(row['Investor Date Added'], '%Y-%m-%d').date()
            )
            session.add(investor)
            investor_mapping[row['Investor Name']] = idx
        
        # Insert commitments
        for _, row in df.iterrows():
            commitment = Commitment(
                investor_id=investor_mapping[row['Investor Name']],
                asset_class=row['Commitment Asset Class'],
                amount=row['Commitment Amount'],
                currency=row['Commitment Currency']
            )
            session.add(commitment)
        
        session.commit()
    
    print(f'Successfully loaded {len(investor_data_sorted)} investors and {len(df)} commitments into database')

if __name__ == '__main__':
    create_database_and_load_data()
