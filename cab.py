from flask import Flask, render_template, request, redirect, url_for, flash
import webbrowser
from database import save_booking
from razorpay_helper import create_order

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

@app.route('/book_cab', methods=['GET', 'POST'])
def book_cab():
    if request.method == 'POST':
        # Get form data
        pickup = request.form.get('pickup')
        drop = request.form.get('drop')
        date = request.form.get('date')
        cab_type = request.form.get('type')
        amount = request.form.get('amount')
        
        # Validate form data
        if not all([pickup, drop, date, cab_type, amount]):
            flash('Please fill all fields', 'error')
            return render_template('book_cab.html')
        
        try:
            amount = int(amount)
            order = create_order(amount, receipt_id="cab123")
            
            # Save booking
            save_booking("demo_user", "cab", pickup, drop, date, cab_type)
            
            # Redirect to payment
            payment_url = f"https://rzp.io/l/{order['id']}"
            webbrowser.open(payment_url)
            
            flash('Cab booked. Razorpay payment initiated.', 'success')
            return redirect(url_for('booking_success'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return render_template('book_cab.html')
    
    return render_template('book_cab.html')

@app.route('/booking_success')
def booking_success():
    return render_template('booking_success.html')

if __name__ == '__main__':
    app.run(debug=True)