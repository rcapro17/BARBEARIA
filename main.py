import psycopg2
from flask import Flask, request, render_template, flash, redirect, g, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flashing messages

def get_db():
    if 'db' not in g:
        # Connect to your PostgreSQL database
        g.db = psycopg2.connect(
            dbname="barbearia",
            user="postgres",
            password="Private@17",
            host="localhost",
            port=5433
        )
    return g.db

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        try:
            db = get_db()
            cur = db.cursor()

            # Execute the SQL INSERT statement
            cur.execute("INSERT INTO client (nome, telefone, email) VALUES (%s, %s, %s)", (nome, telefone, email))

            # Commit the transaction
            db.commit()

            # Close the cursor
            cur.close()

            # Flash message for successful form submission
            flash('success: Form submitted successfully!', 'success')
            return redirect(url_for('register'))
        except Exception as e:
            # Flash message for form submission error
            flash(f'error: An error occurred. Please try again. {str(e)}', 'error')
            return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(debug=True)
