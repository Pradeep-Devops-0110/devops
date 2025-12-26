from flask import Flask, request, jsonify

app = Flask(__name__)

PAYMENTS = []

@app.route("/payment", methods=["POST"])
def process_payment():
    data = request.get_json(force=True)
    payment = {
        "id": len(PAYMENTS) + 1,
        "amount": data.get("amount", 0),
        "currency": data.get("currency", "USD"),
        "status": "processed"
    }
    PAYMENTS.append(payment)
    return jsonify(payment), 201

@app.route("/payments", methods=["GET"])
def list_payments():
    return jsonify(PAYMENTS)

@app.route("/payment/health", methods=["GET"])
def health():
    return "Payment service OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
