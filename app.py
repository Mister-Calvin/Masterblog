import json
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


def load_data(file_path):
  """Loads blog posts from the given JSON file."""
  with open(file_path, "r") as handle:
    return json.load(handle)


def overwrite_data(posts):
    """Overwrites the blog post data in the JSON file."""
    with open("blog_posts.json", "w") as f:
        new_data = json.dump(posts, f, indent=2)
        return new_data


@app.route('/')
def index():
    """Landing Page: Displays all blog posts on the homepage."""
    return render_template('index.html', posts=load_data("blog_posts.json"))


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Displays the add form (GET) and saves a new blog post (POST)."""
    if request.method == 'POST':
        posts = load_data("blog_posts.json")

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')



        new_post = {
            "id": len(posts) + 1,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0
        }

        posts.append(new_post)

        overwrite_data(posts)

        return render_template('sucess_post.html')

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes a blog post by its ID."""
    posts = load_data("blog_posts.json")
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            break

    overwrite_data(posts)

    return render_template('delete_sucess.html')



@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Displays update form (GET) and updates the post content (POST)."""
    posts = load_data("blog_posts.json")

    for info in posts:
        if info['id'] == post_id:
            post = info
            break


    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        #get new data
        new_title = request.form.get('title')
        new_content = request.form.get('content')

        #overwrite old Data with new Data
        post['title'] = new_title
        post['content'] = new_content

        overwrite_data(posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/likes/<int:post_id>', methods=['POST'])
def likes(post_id):
    """Increases the like count of a specific blog post."""
    posts = load_data("blog_posts.json")
    for post in posts:
        if post['id'] == post_id:
            post['likes'] = post['likes'] + 1
            break

    overwrite_data(posts)

    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)