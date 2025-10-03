BlackRock Technical Interview - FastAPI + SQLModel + SQLite Solution

This is a complete solution for the BlackRock take-home assessment.
The application provides REST APIs to manage investor commitments across different asset classes.

==============================================================================
PROJECT STRUCTURE
==============================================================================

blackrock-preqin/
├── README.txt                 									# This file (instructions & setup guide)
├── requirements.txt           									# Python packages
├── data.csv                   									# Source data (provided)
├── db_init.py                									# Database initialization script
├── BlackRock_API_Tests.postman_collection.json                # Postman endpoint tests
└── app/
    ├── main.py               									# FastAPI application
    ├── database.py           									# Database connection setup
    └── models.py             									# SQLModel models

==============================================================================
TECHNOLOGY STACK
==============================================================================

- FastAPI: Modern web framework for building APIs
- SQLModel: Database ORM combining SQLAlchemy and Pydantic
- SQLite: Lightweight database for development
- Pandas: Data processing for CSV loading
- Uvicorn: ASGI server for running the application

==============================================================================
SETUP INSTRUCTIONS FOR WINDOWS
==============================================================================

1. Create and activate virtual environment:
   
   # Open Command Prompt or PowerShell
   python -m venv venv
   venv\Scripts\activate
   
   # You should see (venv) in your prompt

2. Install dependencies:
   
   python -m pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt

3. Place the provided data.csv file in the root directory

4. Initialize database and load data:
   
   python db_init.py
   
   # This creates investors.db and loads all data

5. Start the FastAPI application:
   
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   
   # Application will be available at http://127.0.0.1:8000

==============================================================================
API ENDPOINTS
==============================================================================

The API provides the following endpoints:

1. GET /
   - Root endpoint with API information

2. GET /investors
   - List all investors with total commitments
   - Investors ordered alphabetically by name
   - IDs assigned in alphabetical order (1=Cza Weasley, 2=Ibx Skywalker, etc.)

3. GET /asset-classes
   - Get list of all available asset classes

4. GET /investors/{investor_id}
   - Get detailed investor information with all commitments

5. GET /investors/{investor_id}/summary
   - Get summary statistics by asset class for individual investors

6. GET /investors/{investor_id}/commitments
   - Get commitments for specific investor
   - Optional query parameter: asset_class (filter by asset class)

7. GET /investors/{investor_id}/commitments?asset_class=Hedge%20Funds
   - Get commitments for specific asset class for a specific investor


==============================================================================
INVESTOR ID MAPPING (ALPHABETICAL ORDER)
==============================================================================

ID 1: Cza Weasley fund    (wealth manager, United Kingdom)
ID 2: Ibx Skywalker ltd   (asset manager, United States)  
ID 3: Ioo Gryffindor fund (fund manager, Singapore)
ID 4: Mjd Jedi fund       (bank, China)

==============================================================================
API DOCUMENTATION
==============================================================================

Interactive API documentation is available at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

==============================================================================
DATABASE SCHEMA
==============================================================================

Investors Table:
- id (Primary Key, Integer)
- name (String)
- type (String) 
- country (String)
- date_added (Date)

Commitments Table:
- id (Primary Key, Integer)
- investor_id (Foreign Key to investors.id)
- asset_class (String)
- amount (Float)
- currency (String, always GBP)

==============================================================================
DEACTIVATING VIRTUAL ENVIRONMENT
==============================================================================

When finished, deactivate the virtual environment:

deactivate

==============================================================================
