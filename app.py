from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)


def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)


def overwrite_data(posts):
    with open("blog_posts.json", "w") as f:
        new_data = json.dump(posts, f, indent=2)
        return new_data


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

        overwrite_data(posts)

        return render_template('sucess_post.html')

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_data("blog_posts.json")
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            break

    overwrite_data(posts)

    return render_template('delete_sucess.html')



@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):

    # Fetch the blog posts from the JSON file
    posts = load_data("blog_posts.json")
    #load post
    for info in posts:
        if info['id'] == post_id:
            post = info
            break


    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
    # Update the post in the JSON file
        #get data
        new_title = request.form.get('title')
        new_content = request.form.get('content')
        #overwrite old Data
        post['title'] = new_title
        post['content'] = new_content

        overwrite_data(posts)

        return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route('/likes/<int:post_id>', methods=['POST'])
def likes(post_id):
    posts = load_data("blog_posts.json")
    for post in posts:
        if post['id'] == post_id:
            post['likes'] = post['likes'] + 1
            break

    overwrite_data(posts)

    return redirect(url_for('index'))







if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)