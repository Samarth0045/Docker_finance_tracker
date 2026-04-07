from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os
import json
from datetime import datetime
from werkzeug.exceptions import BadRequest

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'samarth-finance-secret-key-2024'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'finance.db')

# 1. Initialize Database with proper schema
def init_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            description TEXT NOT NULL,
                            amount REAL NOT NULL CHECK(amount > 0),
                            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
            conn.commit()
        print("✅ Database initialized successfully!")
        return True
    except Exception as e:
        print(f"❌ Database init error: {e}")
        return False

# 2. Get Stats (Total, Income, Expense)
def get_stats():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Total balance
            cursor = conn.execute("SELECT SUM(CASE WHEN type='income' THEN amount ELSE -amount END) as total FROM transactions")
            total = cursor.fetchone()[0] or 0
            
            # Income
            cursor = conn.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
            income = cursor.fetchone()[0] or 0
            
            # Expense
            cursor = conn.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
            expense = cursor.fetchone()[0] or 0
            
            # Count
            cursor = conn.execute("SELECT COUNT(*) FROM transactions")
            count = cursor.fetchone()[0]
            
        return {
            "total": round(float(total), 2),
            "income": round(float(income), 2),
            "expense": round(float(expense), 2),
            "count": int(count)
        }
    except Exception as e:
        print(f"❌ Stats error: {e}")
        return {"total": 0, "income": 0, "expense": 0, "count": 0}

# 3. Add Transaction API ✅
@app.route('/api/add', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        desc = data.get('description', '').strip()
        amt = float(data.get('amount', 0))
        t_type = data.get('type', '').strip()
        
        # Validation
        if not desc or len(desc) > 100:
            return jsonify({"error": "Description required (max 100 chars)"}), 400
        if amt <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
        if t_type not in ['income', 'expense']:
            return jsonify({"error": "Type must be 'income' or 'expense'"}), 400
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO transactions (description, amount, type) VALUES (?, ?, ?)", 
                (desc, amt, t_type)
            )
            conn.commit()
        
        print(f"✅ Added: {t_type} ₹{amt} - {desc}")
        return jsonify({"status": "success", "message": f"{t_type.title()} added successfully!"})
    
    except BadRequest:
        return jsonify({"error": "Invalid JSON"}), 400
    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400
    except Exception as e:
        print(f"❌ Add error: {e}")
        return jsonify({"error": "Internal server error"}), 500

# 4. Get History API ✅
@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("""
                SELECT id, description, amount, type, created_at 
                FROM transactions 
                ORDER BY id DESC 
                LIMIT 100
            """)
            rows = cursor.fetchall()
        
        history = []
        for row in rows:
            history.append({
                "id": row[0],
                "description": row[1],
                "amount": float(row[2]),
                "type": row[3],
                "date": row[4][:16] if row[4] else "Just now"
            })
        
        return jsonify({"transactions": history})
    
    except Exception as e:
        print(f"❌ History error: {e}")
        return jsonify({"transactions": [], "error": "Failed to fetch history"}), 500

# 5. Delete Transaction API ✅
@app.route('/api/delete/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # First get the transaction details to update stats
            cursor = conn.execute("SELECT amount, type FROM transactions WHERE id = ?", (transaction_id,))
            result = cursor.fetchone()
            
            if not result:
                return jsonify({"error": "Transaction not found"}), 404
            
            amount, t_type = result
            
            # Delete transaction
            conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            conn.commit()
        
        print(f"✅ Deleted transaction ID: {transaction_id}")
        return jsonify({"status": "success", "message": "Transaction deleted!"})
    
    except Exception as e:
        print(f"❌ Delete error: {e}")
        return jsonify({"error": "Failed to delete"}), 500

# 6. Clear All API ✅
@app.route('/api/clear', methods=['DELETE'])
def clear_all():
    try:
        if request.args.get('confirm') != 'true':
            return jsonify({"error": "Add ?confirm=true to proceed"}), 400
        
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("DELETE FROM transactions")
            conn.commit()
        
        print("✅ All transactions cleared!")
        return jsonify({"status": "success", "message": "All transactions cleared!"})
    
    except Exception as e:
        print(f"❌ Clear error: {e}")
        return jsonify({"error": "Failed to clear"}), 500

# 7. Get Stats API ✅
@app.route('/api/stats', methods=['GET'])
def api_stats():
    stats = get_stats()
    stats["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify(stats)

# 8. Health Check ✅
@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "database": os.path.exists(DB_PATH),
        "timestamp": datetime.now().isoformat()
    })

# 9. Serve Frontend ✅
@app.route('/')
@app.route('/index.html')
def index():
    try:
        return render_template('index.html')
    except:
        # Fallback if no templates folder
        return send_from_directory('.', 'index.html')

# 10. Serve static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Initialize DB
    if init_db():
        print("🚀 Starting Flask app on http://0.0.0.0:5000")
        print("📱 Frontend: http://localhost:5000")
        print("🔧 API Docs: http://localhost:5000/health")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("❌ Failed to initialize database. Exiting...")
        exit(1)
