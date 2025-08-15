from flask import Flask, render_template, request, redirect, url_for, flash
import webbrowser
from database import save_booking
from razorpay_helper import create_order

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for flash messages

@app.route('/book_bus', methods=['GET', 'POST'])
def book_bus():
    if request.method == 'POST':
        # Get form data
        from_city = request.form.get('from_city')
        to_city = request.form.get('to_city')
        date = request.form.get('date')
        seats = request.form.get('seats')
        amount = request.form.get('amount')
        
        # Validate form data
        if not all([from_city, to_city, date, seats, amount]):
            flash('Please fill all fields', 'error')
            return render_template('book_bus.html')
        
        try:
            amount = int(amount)
            order = create_order(amount, receipt_id="bus123")
            
            # Save booking before payment (you might want to change this flow)
            save_booking("demo_user", "bus", from_city, to_city, date, f"{seats} seats")
            
            # Redirect to payment or open in new window
            payment_url = f"https://rzp.io/l/{order['id']}"
            webbrowser.open(payment_url)
            
            flash('Bus booked. Razorpay payment initiated.', 'success')
            return redirect(url_for('booking_success'))
        
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return render_template('book_bus.html')
    
    return render_template('book_bus.html')

@app.route('/booking_success')
def booking_success():
    return render_template('booking_success.html')

if __name__ == '__main__':
    app.run(debug=True)