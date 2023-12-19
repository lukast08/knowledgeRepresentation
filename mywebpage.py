from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    title = 'Welcome to Our Website!'
    return render_template('home.html', title=title)

@app.route('/about/')
def about():
    return 'This is the about page'

if __name__ == '__main__':
    app.run(debug=True)