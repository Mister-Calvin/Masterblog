from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)


def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)


@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=load_data("blog_posts.json"))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_data("blog_posts.json")

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')


        new_post = {
            "id": len(posts) + 1,
            "author": author,
            "title": title,
            "content": content
        }

        posts.append(new_post)

        with open("blog_posts.json", "w") as f:
            json.dump(posts, f, indent=2)

        return render_template('sucess_post.html')

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_data("blog_posts.json")
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            break

    with open("blog_posts.json", "w") as f:
        json.dump(posts, f, indent=2)

    return render_template('delete_sucess.html')









if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)