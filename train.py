from flask import Flask, render_template, request, redirect, url_for, flash
import webbrowser
from database import save_booking
from razorpay_helper import create_order

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

@app.route('/book_train', methods=['GET', 'POST'])
def book_train():
    if request.method == 'POST':
        # Get form data
        from_city = request.form.get('from_city')
        to_city = request.form.get('to_city')
        date = request.form.get('date')
        train_class = request.form.get('class')
        amount = request.form.get('amount')
        
        # Validate form data
        if not all([from_city, to_city, date, train_class, amount]):
            flash('Please fill all fields', 'error')
            return render_template('book_train.html')
        
        try:
            amount = int(amount)
            # Create Razorpay order
            order = create_order(amount, receipt_id="train123")
            
            # Save booking to database
            save_booking("demo_user", "train", from_city, to_city, date, train_class)
            
            # Open payment link (works when running locally)
            payment_url = f"https://rzp.io/l/{order['id']}"
            webbrowser.open(payment_url)
            
            flash('Train booked successfully. Payment link opened in new tab.', 'success')
            return redirect(url_for('booking_success'))
        
        except ValueError:
            flash('Invalid amount. Please enter a valid number.', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
        
        return render_template('book_train.html')
    
    return render_template('book_train.html')

@app.route('/booking_success')
def booking_success():
    return render_template('booking_success.html')

if __name__ == '__main__':
    app.run(debug=True)