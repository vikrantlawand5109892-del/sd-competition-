from flask import Flask, render_template, request, redirect, url_for, flash
import webbrowser
from database import save_booking
from razorpay_helper import create_order

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

@app.route('/book_hotel', methods=['GET', 'POST'])
def book_hotel():
    if request.method == 'POST':
        # Get form data
        city = request.form.get('city')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        room_type = request.form.get('room')
        amount = request.form.get('amount')
        
        # Validate form data
        if not all([city, checkin, checkout, room_type, amount]):
            flash('Please fill all fields', 'error')
            return render_template('book_hotel.html')
        
        try:
            amount = int(amount)
            # Create Razorpay order
            order = create_order(amount, receipt_id="hotel123")
            
            # Save booking to database
            booking_details = f"{room_type} till {checkout}"
            save_booking("demo_user", "hotel", city, city, checkin, booking_details)
            
            # Open payment link (works when running locally)
            payment_url = f"https://rzp.io/l/{order['id']}"
            webbrowser.open(payment_url)
            
            flash('Hotel booked successfully. Payment link opened in new tab.', 'success')
            return redirect(url_for('booking_success'))
        
        except ValueError:
            flash('Invalid amount. Please enter a valid number.', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return render_template('book_hotel.html')
    
    return render_template('book_hotel.html')

@app.route('/booking_success')
def booking_success():
    return render_template('booking_success.html')

if __name__ == '__main__':
    app.run(debug=True)