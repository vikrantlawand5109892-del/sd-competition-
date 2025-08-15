from flask import Flask, render_template, request, redirect, url_for, flash
import webbrowser
from database import save_booking
from razorpay_helper import create_order

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

@app.route('/book_flight', methods=['GET', 'POST'])
def book_flight():
    if request.method == 'POST':
        # Get form data
        from_city = request.form.get('from_city')
        to_city = request.form.get('to_city')
        date = request.form.get('date')
        flight_class = request.form.get('class')
        amount = request.form.get('amount')
        
        # Validate form data
        if not all([from_city, to_city, date, flight_class, amount]):
            flash('Please fill all fields', 'error')
            return render_template('book_flight.html')
        
        try:
            amount = int(amount)
            # Create Razorpay order
            order = create_order(amount, receipt_id="flight123")
            
            # Save booking to database
            save_booking("demo_user", "flight", from_city, to_city, date, flight_class)
            
            # Open payment link (note: this will only work if server is running locally)
            payment_url = f"https://rzp.io/l/{order['id']}"
            webbrowser.open(payment_url)
            
            flash('Flight booked successfully. Payment link opened in new tab.', 'success')
            return redirect(url_for('booking_success'))
        
        except ValueError:
            flash('Invalid amount. Please enter a valid number.', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return render_template('book_flight.html')
    
    return render_template('book_flight.html')

@app.route('/booking_success')
def booking_success():
    return render_template('booking_success.html')

if __name__ == '__main__':
    app.run(debug=True)