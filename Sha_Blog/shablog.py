from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    {
        'author': 'Corey Bee',
        'title': 'Blog Post 1',
        'content': 'First post content.',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Mei Honey',
        'title': 'Blog Post 2',
        'content': 'Second post content.',
        'date_posted': 'April 25, 2018'
    },
    {
        'author': 'Corey Bee',
        'title': 'Blog Post 3',
        'content': 'Third post content.',
        'date_posted': 'May 20, 2018'
    }
]

# you can have more than one route
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')


# if we don't want to use environment variables
# for a debug mode, we can also write
if __name__ == '__main__':
    app.run(debug=True)
