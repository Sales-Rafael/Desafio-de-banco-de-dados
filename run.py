from flask import Flask, request, jsonify
import sqlite3
import json
from math import sqrt

app = Flask(__name__)

# Configuração do banco de dados SQLite
DATABASE = 'partners.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS partners
                 (id TEXT PRIMARY KEY,
                 trading_name TEXT,
                 owner_name TEXT,
                 document TEXT UNIQUE,
                 coverage_area TEXT,
                 address TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/partners', methods=['POST'])
def create_partner():
    try:
        data = request.get_json()
        
        # Validação básica
        required_fields = ['id', 'tradingName', 'ownerName', 'document', 'coverageArea', 'address']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Verifica se documento já existe
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT 1 FROM partners WHERE document=?", (data['document'],))
        if c.fetchone():
            conn.close()
            return jsonify({"error": "Document already exists"}), 400
        
        # Insere no banco de dados
        c.execute("INSERT INTO partners VALUES (?, ?, ?, ?, ?, ?)",
                 (data['id'],
                  data['tradingName'],
                  data['ownerName'],
                  data['document'],
                  json.dumps(data['coverageArea']),
                  json.dumps(data['address'])))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "Partner created", "id": data['id']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/partners/<partner_id>', methods=['GET'])
def get_partner(partner_id):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM partners WHERE id=?", (partner_id,))
        partner = c.fetchone()
        conn.close()
        
        if not partner:
            return jsonify({"error": "Partner not found"}), 404
            
        return jsonify({
            "id": partner[0],
            "tradingName": partner[1],
            "ownerName": partner[2],
            "document": partner[3],
            "coverageArea": json.loads(partner[4]),
            "address": json.loads(partner[5])
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/partners/search', methods=['GET'])
def search_partner():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM partners")
        all_partners = c.fetchall()
        conn.close()
        
        nearest = None
        min_distance = float('inf')
        
        for partner in all_partners:
            address = json.loads(partner[5])
            px, py = address['coordinates']
            
            # Cálculo de distância simplificado (para pequenas distâncias)
            distance = sqrt((px - lng)**2 + (py - lat)**2)
            
            if distance < min_distance:
                min_distance = distance
                nearest = partner
        
        if not nearest:
            return jsonify({"error": "No partners found"}), 404
            
        return jsonify({
            "id": nearest[0],
            "tradingName": nearest[1],
            "ownerName": nearest[2],
            "document": nearest[3],
            "coverageArea": json.loads(nearest[4]),
            "address": json.loads(nearest[5])
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)