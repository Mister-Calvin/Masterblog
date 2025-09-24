from flask import Flask, render_template, request

app = Flask(__name__)

import json


def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)




@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=load_data("blog_posts.json"))





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)