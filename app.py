from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import bcrypt
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print(f"Connected to MongoDB at {MONGO_URI}")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise

db = client['todo_db']
users_collection = db['users']
tasks_collection = db['tasks']
categories_collection = db['categories']

# Create indexes
users_collection.create_index('username', unique=True)
tasks_collection.create_index('user_id')
tasks_collection.create_index('category')

@app.route('/')
def index():
    return render_template('index.html')

# Auth endpoints
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if users_collection.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        'username': username,
        'password': hashed,
        'created_at': datetime.utcnow()
    }
    result = users_collection.insert_one(user)
    
    access_token = create_access_token(identity=str(result.inserted_id))
    return jsonify({'access_token': access_token, 'username': username}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = users_collection.find_one({'username': username})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({'access_token': access_token, 'username': username}), 200

# Task endpoints
@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    category = request.args.get('category')
    status = request.args.get('status')
    search = request.args.get('search')
    
    query = {'user_id': user_id}
    if category and category != 'all':
        query['category'] = category
    if status == 'completed':
        query['completed'] = True
    elif status == 'pending':
        query['completed'] = False
    if search:
        query['title'] = {'$regex': search, '$options': 'i'}
    
    tasks = list(tasks_collection.find(query).sort('created_at', -1))
    for task in tasks:
        task['_id'] = str(task['_id'])
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.json
    
    task = {
        'user_id': user_id,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'category': data.get('category', 'general'),
        'priority': data.get('priority', 'medium'),
        'due_date': data.get('due_date'),
        'completed': False,
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
    result = tasks_collection.insert_one(task)
    task['_id'] = str(result.inserted_id)
    return jsonify(task), 201

@app.route('/api/tasks/<task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.json
    
    update_data = {'updated_at': datetime.utcnow()}
    if 'title' in data:
        update_data['title'] = data['title']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'category' in data:
        update_data['category'] = data['category']
    if 'priority' in data:
        update_data['priority'] = data['priority']
    if 'due_date' in data:
        update_data['due_date'] = data['due_date']
    if 'completed' in data:
        update_data['completed'] = data['completed']
    
    result = tasks_collection.update_one(
        {'_id': ObjectId(task_id), 'user_id': user_id},
        {'$set': update_data}
    )
    
    if result.matched_count == 0:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'message': 'Task updated'})

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    result = tasks_collection.delete_one({'_id': ObjectId(task_id), 'user_id': user_id})
    
    if result.deleted_count == 0:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({'message': 'Task deleted'})

# Category endpoints
@app.route('/api/categories', methods=['GET'])
@jwt_required()
def get_categories():
    user_id = get_jwt_identity()
    categories = list(categories_collection.find({'user_id': user_id}))
    for cat in categories:
        cat['_id'] = str(cat['_id'])
    return jsonify(categories)

@app.route('/api/categories', methods=['POST'])
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    data = request.json
    
    category = {
        'user_id': user_id,
        'name': data.get('name'),
        'color': data.get('color', '#3b82f6'),
        'created_at': datetime.utcnow()
    }
    result = categories_collection.insert_one(category)
    category['_id'] = str(result.inserted_id)
    return jsonify(category), 201

# Statistics endpoint
@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = get_jwt_identity()
    
    total = tasks_collection.count_documents({'user_id': user_id})
    completed = tasks_collection.count_documents({'user_id': user_id, 'completed': True})
    pending = total - completed
    
    # Tasks by category
    pipeline = [
        {'$match': {'user_id': user_id}},
        {'$group': {'_id': '$category', 'count': {'$sum': 1}}}
    ]
    by_category = list(tasks_collection.aggregate(pipeline))
    
    # Overdue tasks
    overdue = tasks_collection.count_documents({
        'user_id': user_id,
        'completed': False,
        'due_date': {'$lt': datetime.utcnow().isoformat()}
    })
    
    return jsonify({
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'by_category': by_category
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
