# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## Testing

The project includes a comprehensive test suite with 30 tests covering all API endpoints and edge cases.

### Run Tests

1. Install dependencies (including test dependencies):

   ```bash
   pip install -r requirements.txt
   ```

2. Run all tests:

   ```bash
   pytest tests/ -v
   ```

3. Run tests with coverage report:

   ```bash
   pytest tests/ --cov=src --cov-report=term-missing
   ```

### Test Organization

- **tests/test_activities.py** — Tests for GET /activities endpoint
- **tests/test_signup.py** — Tests for POST signup endpoint
- **tests/test_unregister.py** — Tests for DELETE unregister endpoint
- **tests/test_root.py** — Tests for root endpoint redirects
- **tests/test_integration.py** — Multi-step workflow integration tests

Current test coverage: **100%** ✅

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/signup?email=student@mergington.edu` | Unregister from an activity                                         |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
