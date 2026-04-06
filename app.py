from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database initialize karna
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT, status TEXT)')
    conn.close()

init_db()

# Home page - HTML serve karega
@app.route('/')
def index():
    return render_template('index.html')

# API: Saari tasks get karna
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('database.db')
    cursor = conn.execute('SELECT id, name, status FROM tasks')
    tasks = [{'id': row[0], 'name': row[1], 'status': row[2]} for row in cursor]
    conn.close()
    return jsonify(tasks)

# API: Naya task add karna
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    name = data.get('name')
    conn = sqlite3.connect('database.db')
    conn.execute('INSERT INTO tasks (name, status) VALUES (?, ?)', (name, 'pending'))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added'}), 201

# API: Task delete karna
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('database.db')
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted'})

# API: Task complete karna
@app.route('/api/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    conn = sqlite3.connect('database.db')
    conn.execute('UPDATE tasks SET status = ? WHERE id = ?', ('completed', task_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task completed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)