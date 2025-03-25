# Student Management System - FastAPI Backend

![FastAPI Logo](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png) 

A RESTful API for managing student records built with FastAPI and SQLite. This backend provides endpoints for creating and retrieving student information with proper validation and error handling.

## Features

### 📝 Core Functionalities
- **Student creation** with auto-generated IDs
- **Student retrieval** by ID
- **List all students** in the system
- **Data validation** for all inputs
- **Duplicate email prevention**

### 🛡️ Data Integrity
- **SQLite database** for persistent storage
- **Automatic database initialization** on startup
- **ORM-based operations** using SQLAlchemy
- **Proper error handling** for various scenarios

### 📊 API Features
- **Standard REST endpoints** following best practices
- **Request/response validation** with Pydantic models
- **Interactive API documentation** (Swagger UI & ReDoc)
- **Proper HTTP status codes** for all responses

## API Endpoints

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|--------------|----------|
| `/students/` | POST | Create a new student | `{"name": str, "age": int, "email": str}` | Created student data with ID |
| `/students/{student_id}` | GET | Get a specific student | - | Student data |
| `/students/` | GET | Get all students | - | List of all students |

## Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLite** - Lightweight database for storage
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Pydantic** - Data validation and settings management
- **Uvicorn** - ASGI server for running FastAPI

## Getting Started

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/your-username/student-management-api.git
   cd student-management-api
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

1. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

2. The server will start at `http://127.0.0.1:8000`

3. Access the interactive documentation:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Database Initialization

The SQLite database (`students.db`) is automatically created when you first run the application. The database file will be created in your project directory.

## Example Requests

### Create a new student
```bash
curl -X POST "http://localhost:8000/students/" \
-H "Content-Type: application/json" \
-d '{"name": "John Doe", "age": 21, "email": "john.doe@example.com"}'
```

### Get a student by ID
```bash
curl "http://localhost:8000/students/1"
```

### Get all students
```bash
curl "http://localhost:8000/students/"
```

## Error Handling

The API returns appropriate HTTP status codes with error details:
- `400 Bad Request` - Invalid input data or duplicate email
- `404 Not Found` - Requested student doesn't exist
- `422 Unprocessable Entity` - Validation error

## Testing

You can test the API using:
1. The built-in interactive documentation (Swagger UI)
2. Tools like Postman or Insomnia
3. curl commands as shown above

## Future Enhancements

- Add authentication and authorization
- Implement update and delete endpoints
- Add pagination for student list
- Include search/filter functionality
- Add more student fields (e.g., enrollment date, courses)
- Implement proper logging
