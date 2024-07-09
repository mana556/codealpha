from flask import Flask, request, render_template_string
import sqlite3
import subprocess

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name LIKE '%" + query + "%'")
    results = c.fetchall()
    conn.close()
    return render_template_string('''
        <h1>Search Results</h1>
        <ul>
            {% for row in results %}
                <li>{{ row }}</li>
            {% endfor %}
        </ul>
        <a href="/">Go back</a>
    ''', results=results)

@app.route('/user/<username>')
def user_profile(username):
    return render_template_string('<h1>User: {{ username }}</h1>')

@app.route('/run_command', methods=['POST'])
def run_command():
    command = request.form['command']
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return render_template_string('<pre>{{ result.stdout }}</pre>')

if __name__ == '__main__':
    app.run(debug=True)
