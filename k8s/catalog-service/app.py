from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/catalog", methods=["GET"])
def get_catalog():
    return jsonify([
        {"id": 1, "name": "Phone", "price": 499.99},
        {"id": 2, "name": "Laptop", "price": 1299.00},
        {"id": 3, "name": "Headphones", "price": 99.00},
    ])

@app.route("/catalog/health", methods=["GET"])
def health():
    return "Catalog service OK", 200

if __name__ == "__main__":
    # IMPORTANT: must match Kubernetes service port
    app.run(host="0.0.0.0", port=8080)
