from flask import Flask

# instantiate the object of the class flask
app = Flask(__name__)

# creating our first route as home page
@app.route('/')
def home():
    return 'Homepage content'

@app.route('/about/')
def about():
    return 'About content goes here'

if __name__ == "__main__":
    app.run(debug=True)