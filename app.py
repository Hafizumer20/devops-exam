from flask import Flask, render_template, request, jsonify
import os
import sqlite3

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT, status TEXT)')
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute('SELECT id, name, status FROM tasks')
    tasks = [{'id': row[0], 'name': row[1], 'status': row[2]} for row in cursor]
    conn.close()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Task name is required'}), 400

    name = data.get('name').strip()
    if not name:
        return jsonify({'error': 'Task name is required'}), 400

    conn = sqlite3.connect(DB_PATH)
    conn.execute('INSERT INTO tasks (name, status) VALUES (?, ?)', (name, 'pending'))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added'}), 201

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})

@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute('UPDATE tasks SET status = ? WHERE id = ?', ('completed', task_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task completed'})


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response


@app.route('/api/<path:dummy>', methods=['OPTIONS'])
def handle_api_preflight(dummy):
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)