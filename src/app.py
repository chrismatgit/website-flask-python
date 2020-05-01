from flask import Flask, render_template

# instantiate the object of the class flask
app = Flask(__name__)

# creating our first route as home page
@app.route('/')
def home():
    # render_tempalte help to access different html pages
    return render_template('home.html')

# creating the route that will handle the
@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN  # Content Delivery Network

    start = datetime.datetime(2016, 3, 1)
    end = datetime.datetime(2016, 5, 10)

    df = data.DataReader(name="GOOG", data_source="yahoo",
                         start=start, end=end)

    # function to check the increase and decrease value
    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open+df.Close)/2
    df["Height"] = abs(df.Close-df.Open)
    # drawing the plot now
    p = figure(x_axis_type='datetime', width=1000, height=300)
    p.title.text = "Candlestick chart"
    # transparent grid
    p.grid.grid_line_alpha = 0.3

    '''
    drawing the rectangle
    @param x coordinator
    @param y coordinator
    @param width of the rectangle
    @param height of the rectangle
    @param 5 and 6 are color property
    '''
    # twelve hours in milisecond
    hours_12 = 12*60*60*1000

    # glyph for the vertical lines
    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
           hours_12, df.Height[df.Status == "Increase"],
           fill_color="#CCFFFF", line_color="black")

    # day open with higher price and close with the lower price
    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
           hours_12, df.Height[df.Status == "Decrease"],
           fill_color="#FF3333", line_color="black")

    # generate the html and the script of the bokeh chart
    script1, div1 = components(p)

    # generate the javascript file and the css in order to add them into our html
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files

    # output the candlestick
    # output_file("candlestcik.html")
    # show(p)
    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js)


@app.route('/about/')
def about():
    # rendering the about page
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
