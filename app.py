from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'finance.db'

# 1. Database Initialize kara
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS transactions 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         description TEXT, 
                         amount REAL, 
                         type TEXT)''')
    print("Database Initialized!")

# 2. Add Entry API
@app.route('/add', methods=['POST'])
def add_transaction():
    data = request.json
    desc = data.get('description')
    amt = data.get('amount')
    t_type = data.get('type') # 'income' or 'expense'

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO transactions (description, amount, type) VALUES (?, ?, ?)", 
                     (desc, amt, t_type))
    return jsonify({"status": "success"})

# 3. Get History API
@app.route('/history', methods=['GET'])
def get_history():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT description, amount, type FROM transactions ORDER BY id DESC")
        rows = cursor.fetchall()
    
    history = [{"description": r[0], "amount": r[1], "type": r[2]} for r in rows]
    return jsonify(history)

# 4. Main Page load kara
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    # Port 5000 var run kara
    app.run(host='0.0.0.0', port=5000)
