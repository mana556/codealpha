from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name LIKE ?", ('%' + query + '%',))
    results = c.fetchall()
    conn.close()
    return render_template('search_results.html', results=results)

@app.route('/user/<username>')
def user_profile(username):
    return render_template('user_profile.html', username=username)

if __name__ == '__main__':
    app.run(debug=False)
