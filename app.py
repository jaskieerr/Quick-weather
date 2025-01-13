from flask import Flask, render_template , url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index_0.html")

@app.route('/login')
def login():
    pass

if __name__ == '__main__':
    app.run(debug=True)