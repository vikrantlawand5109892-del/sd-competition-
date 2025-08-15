from flask import Flask, request, jsonify
import razorpay

app = Flask(__name__)

# 🔐 Replace these with your real test/live Razorpay API keys
app.config['RAZORPAY_KEY_ID'] = "rzp_test_yourKey"
app.config['RAZORPAY_KEY_SECRET'] = "yourSecret"

# Initialize Razorpay client
client = razorpay.Client(auth=(app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET']))

@app.route('/api/create_order', methods=['POST'])
def create_order():
    try:
        # Get data from request
        data = request.json
        amount = data.get('amount')
        receipt_id = data.get('receipt_id', "TXN001")  # Default receipt ID
        
        if not amount:
            return jsonify({"error": "Amount is required"}), 400
        
        # Create Razorpay order
        order = client.order.create({
            "amount": int(amount) * 100,  # Convert rupees to paise
            "currency": "INR",
            "receipt": receipt_id,
            "payment_capture": 1
        })
        
        return jsonify({
            "success": True,
            "order": order,
            "key": app.config['RAZORPAY_KEY_ID']  # Send key to frontend
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)