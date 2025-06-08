from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
POSTS_FILE = 'posts.json'

def load_posts():
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, 'r') as f:
        return json.load(f)
    
def save_posts(posts):
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

@app.route('/')
def index():
    posts = load_posts()
    posts = sorted(posts, key=lambda x: x['date'], reverse=True)
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return render_template('post.html', post=post)
    return "Post not found.", 404

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        posts = load_posts()
        new_id = max([p['id'] for p in posts], default = 0) + 1
        title = request.form['title']
        content = request.form['content']
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post = {'id': new_id, 'title': title, 'content': content, 'date': date_str}

        posts.append(post)
        save_posts(posts)
        return redirect(url_for('index'))
    return render_template('new_post.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

