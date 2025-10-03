BlackRock Technical Interview - FastAPI + SQLModel + SQLite Solution

This is a complete solution for the BlackRock take-home assessment.
The application provides REST APIs to manage investor commitments across different asset classes.

==============================================================================
PROJECT STRUCTURE
==============================================================================

blackrock-preqin/
├── README.txt                 # This file (instructions & setup guide)
├── requirements.txt           # Python packages
├── data.csv                   # Source data (provided)
├── db_init.py                # Database initialization script
└── app/
    ├── main.py               # FastAPI application
    ├── database.py           # Database connection setup
    └── models.py             # SQLModel models

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

3. GET /investors/{investor_id}/commitments
   - Get commitments for specific investor
   - Optional query parameter: asset_class (filter by asset class)

4. GET /investors/{investor_id}
   - Get detailed investor information with all commitments

5. GET /asset-classes
   - Get list of all available asset classes

6. GET /commitments/summary
   - Get summary statistics by asset class

==============================================================================
TESTING WITH POSTMAN
==============================================================================

1. Download and install Postman from https://www.postman.com/downloads/

2. Import the following requests into Postman:

   Collection Name: BlackRock Preqin API Tests

   Request 1: Get All Investors
   - Method: GET
   - URL: http://127.0.0.1:8000/investors
   - Description: Returns all investors with total commitments

   Request 2: Get Investor Commitments
   - Method: GET  
   - URL: http://127.0.0.1:8000/investors/1/commitments
   - Description: Get commitments for Cza Weasley fund (ID 1)

   Request 3: Filter Commitments by Asset Class
   - Method: GET
   - URL: http://127.0.0.1:8000/investors/2/commitments?asset_class=Hedge Funds
   - Description: Get Hedge Fund commitments for Ibx Skywalker ltd (ID 2)

   Request 4: Get Investor Details
   - Method: GET
   - URL: http://127.0.0.1:8000/investors/3
   - Description: Get detailed info for Ioo Gryffindor fund (ID 3)

   Request 5: Get Asset Classes
   - Method: GET
   - URL: http://127.0.0.1:8000/asset-classes
   - Description: List all available asset classes

   Request 6: Get Summary Statistics
   - Method: GET
   - URL: http://127.0.0.1:8000/commitments/summary
   - Description: Get summary by asset class

3. Test each endpoint and verify the responses

4. Try different investor IDs (1-4) and asset class filters:
   - Asset classes: "Hedge Funds", "Private Equity", "Real Estate", 
     "Infrastructure", "Natural Resources", "Private Debt"

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
- last_updated (Date)

Commitments Table:
- id (Primary Key, Integer)
- investor_id (Foreign Key to investors.id)
- asset_class (String)
- amount (Float, in millions)
- currency (String, always GBP)

==============================================================================
DESIGN DECISIONS
==============================================================================

1. SQLModel Choice: Combines SQLAlchemy ORM power with Pydantic validation
2. Alphabetical ID Assignment: Provides predictable, stable investor IDs
3. Amount in Millions: Easier to read large numbers (58.0 vs 58000000)
4. Separate Tables: Normalized design reduces redundancy
5. Error Handling: Proper HTTP status codes (404 for not found)
6. Query Parameters: Flexible filtering by asset class

==============================================================================
DEACTIVATING VIRTUAL ENVIRONMENT
==============================================================================

When finished, deactivate the virtual environment:

deactivate

==============================================================================
NOTES
==============================================================================

- SQLite database (investors.db) is created locally
- All amounts are in GBP millions for readability
- API follows RESTful conventions
- Full type annotations for better IDE support
- Comprehensive error handling with meaningful messages
