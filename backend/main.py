from flask import Flask, jsonify
from pymongo import MongoClient # type: ignore
import requests # type: ignore
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Replace with your MongoDB Atlas connection string
client = MongoClient('mongodb+srv://mayankuchariya0:mayank123@cluster0.u0zlvya.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['nobero_database']
collection = db['products']


@app.route('/products', methods=['GET'])
def get_products():
    data = list(collection.find({}, {'_id': 0}))  # Exclude the MongoDB _id field
    return jsonify(data)


@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    try:
        data = collection.find_one({"id": int(id)}, {'_id': 0})  # Exclude the MongoDB _id field
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
