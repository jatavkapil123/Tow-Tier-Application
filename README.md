# Two-Tier Todo Application

A simple two-tier application with Python Flask backend and MongoDB database.

## Architecture

- **Tier 1 (Frontend)**: HTML/CSS/JavaScript interface
- **Tier 2 (Backend)**: Flask REST API with MongoDB

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MongoDB (if not running):
```bash
mongod
```

3. Run the application:
```bash
python app.py
```

4. Open browser at: http://localhost:5000

## Environment Variables

- `MONGO_URI`: MongoDB connection string (default: mongodb://localhost:27017/)

## API Endpoints

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/<id>` - Update task status
- `DELETE /api/tasks/<id>` - Delete a task
