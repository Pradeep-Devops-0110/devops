from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ORDERS = []
CATALOG_URL = "http://catalog-service:8080/catalog"

@app.route("/order", methods=["POST"])
def create_order():
    data = request.get_json(force=True)

    # Fetch catalog items from catalog-service
    catalog_items = requests.get(CATALOG_URL).json()

    order = {
        "id": len(ORDERS) + 1,
        "items": data.get("items", catalog_items),  # fallback to catalog if no items provided
        "total": data.get("total", 0)
    }
    ORDERS.append(order)
    return jsonify(order), 201

@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(ORDERS)

@app.route("/order/health", methods=["GET"])
def health():
    return "Order service OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
