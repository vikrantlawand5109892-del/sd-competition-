from flask import Flask, render_template, request, redirect, url_for, flash
from gemini_client import ask_gemini
from multilingual_assistant import speak
from booking import bus, train, flight, cab, hotel

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    query = request.form.get('query')
    if not query:
        flash('Please enter your travel query', 'error')
        return redirect(url_for('home'))
    
    try:
        response = ask_gemini(f"You are an expert AI travel planner. Plan this trip: {query}")
        return render_template('trip_plan.html', plan=response)
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('home'))

@app.route('/book_bus')
def book_bus():
    return bus.book_bus()

@app.route('/book_train')
def book_train():
    return train.book_train()

@app.route('/book_flight')
def book_flight():
    return flight.book_flight()

@app.route('/book_cab')
def book_cab():
    return cab.book_cab()

@app.route('/book_hotel')
def book_hotel():
    return hotel.book_hotel()

@app.route('/ask_assistant')
def ask_assistant():
    try:
        speak("What can I help you with today?")
        flash("Assistant is ready to help. What can I help you with today?", 'info')
    except Exception as e:
        flash(f"Assistant error: {str(e)}", 'error')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)