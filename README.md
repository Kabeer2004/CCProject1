# Cloud Computing Course Project - 6th Semester Engineering

This repository contains two separate projects developed as part of the **Cloud Computing** course in my 6th Semester of Engineering:

1. **Frontend**: Pomodoro Tracker (Next.js application)
2. **Backend**: Student Management System (FastAPI application)

## Project Overview

### 🎯 Frontend: Pomodoro Tracker
A productivity timer application implementing the Pomodoro Technique with customizable work/break sessions.

**Key Features**:
- Interactive countdown timer with circular progress visualization
- Start/Pause/Reset functionality
- Customizable session durations
- Responsive design with Tailwind CSS

### ⚙️ Backend: Student Management System
A RESTful API for managing student records with SQLite database.

**Key Features**:
- Create and retrieve student records
- Data validation and error handling
- Automatic database initialization
- Interactive API documentation

## Updated Project Structure

```
cloud-computing-project/
├── backend/
│   ├── student-management/
│   │   ├── .gitignore
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── requirements.txt
│   │   └── students.db
│   └── README.md
│
├── frontend/
│   ├── pomodoro-tracker/
│   │   ├── app/
│   │   │   ├── favicon.ico
│   │   │   ├── globals.css
│   │   │   ├── layout.js
│   │   │   └── page.js
│   │   ├── .gitignore
│   │   ├── jsconfig.json
│   │   ├── next.config.mjs
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   ├── postcss.config.mjs
│   │   └── README.md
│   └── README.md
│
└── README.md
```

## Technologies Used

| Component | Technologies |
|-----------|--------------|
| **Frontend** | Next.js 13+, React, Tailwind CSS, JavaScript |
| **Backend** | FastAPI, Python, SQLite, SQLAlchemy, Pydantic |

## Getting Started

### Frontend Setup
1. Navigate to `frontend/pomodoro-tracker` directory
2. Install dependencies: `npm install`
3. Run development server: `npm run dev`
4. Access at: `http://localhost:3000`

### Backend Setup
1. Navigate to `backend/student-management` directory
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Run server: `uvicorn main:app --reload`
6. Access API docs at: `http://localhost:8000/docs`

## Key Learnings

Through this project, I gained practical experience with:
- Building responsive frontend applications with modern frameworks
- Designing RESTful APIs with proper endpoints
- Database integration and ORM usage
- Application state management
- Project architecture and separation of concerns
- Cloud computing concepts in practice

## Future Enhancements

Potential improvements for both projects:
- **Frontend**: Add user authentication, task tracking, cloud deployment
- **Backend**: Implement full CRUD operations, add authentication, deploy to cloud, add a frontend and expand functionality to create a full Student Management System

## Course Relevance

This project helped demonstrate several cloud computing concepts:
- Client-server architecture
- API design and consumption
- Database management
- Potential for cloud deployment
- Scalability considerations

---

*Developed by Kabeer Ahmed Merchant as part of the Cloud Computing course - 6th Semester Engineering*
