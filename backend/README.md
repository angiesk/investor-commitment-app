# FastAPI Investor-User Application

This project demonstrates a basic FastAPI app that models user types and investors.

## Features
- Two user types: `preqin` and `investor`.
- Investors are linked to users of type `investor`.
- SQLite database for persistent storage.

## Installation

1. Clone the project:
   ```bash
   git clone <repo-url>
   ```
2. Navigate to the directory and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

4. Access the API at `http://127.0.0.1:8000`.

## API Endpoints

### Users
- **Create User**: `POST /users`
- **Get User**: `GET /users/{user_id}`

### Investors
- **Create Investor**: `POST /investors`
- **Get Investor**: `GET /investors/{investor_id}`

### Commitments
- **Create Commitments**
- **Get commitments for investor id `GET /investors/{investor_id}/commitments`

### Data migration script to load data into database
- creates users,investors and commitments based on data from data.csv

## Swagger doc
http://127.0.0.1:8000/docs