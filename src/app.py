from flask import Flask, render_template

# instantiate the object of the class flask
app = Flask(__name__)

# creating our first route as home page
@app.route('/')
def home():
    # render_tempalte help to access different html pages
    return render_template('home.html')

@app.route('/about/')
def about():
    # rendering the about page
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)