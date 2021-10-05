from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__)


@app.route("/")
def get_home():
    return render_template('index.html')


@app.route("/jobs")
def get_jobs():
    return render_template('job-listing.html')


if __name__ == "__main__":
    app.run(debug=True)
