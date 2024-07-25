# python_backend_assignment

# Wellness Retreat Backend Service

This is a Flask-based backend service for managing retreat data for a wellness retreat platform. It provides APIs for retrieving, creating, and booking retreats.

## Prerequisites

- Python 3.8+
- PostgreSQL

## Setup

1. Clone the repository:
   git clone https://github.com/Sanchit24s/python_backend_assignment.git
   cd python_backend_assignment

2. Create a virtual environment and activate it:
   python -m venv venv
   source venv/bin/activate # On Windows use venv\Scripts\activate

3. Install the required packages:
   pip install -r requirements.txt

4. Set up your environment variables:
   Create a `.env` file in the root directory with the following contents:
   SQLALCHEMY_TRACK_MODIFICATIONS=False
   DATABASE_URL=postgresql://username:password@localhost/wellness_retreat
   SECRET_KEY=your_secret_key_here
   Replace `username`, `password`, and `localhost` with your PostgreSQL credentials, and set a strong, random string for SECRET_KEY.

5. Run the application:
   python run.py
   The server will start running on http://localhost:5000.
   This application provides the following endpoints:

   GET /retreats: Fetch retreats with filtering, pagination, and search capabilities.
   POST /retreats: Create a new retreat.
   POST /book: Book a retreat.
   GET /bookings: Fetch retreat bookings.
