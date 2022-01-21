import random, string
from cv2 import meanShift
from flask import Flask, render_template, redirect, url_for, request, jsonify
from pathlib import Path
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
from models import Post, Message, User
import pyrebase

path = Path(__file__).parent

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '4864885245-Key-AppPost'

config = {
    "apiKey": "AIzaSyCF2KAx6z0opLtVXsQrgSRHgoi4D8R8YPs",
    "authDomain": "flask-post-7af5b.firebaseapp.com",
    "databaseURL": "https://flask-post-7af5b-default-rtdb.europe-west1.firebasedatabase.app/",
    "storageBucket": "projectId.appspot.com",
    "serviceAccount": path / "key.json"
}

cred = credentials.Certificate(path / 'key.json')
default_app = initialize_app(cred)
db = firestore.client()
fb = pyrebase.initialize_app(config)
# db = fb.database()
posts_ref = db.collection('posts')
users_ref = db.collection('users')

auth = fb.auth()

@app.route('/home')
@app.route('/')
def index():
    try:
        todo_id = request.args.get('id')    
        if todo_id:
            todo = posts_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_posts = [doc.to_dict() for doc in posts_ref.stream()]
            posts = []
            for post in all_posts:
                postc = Post(post['title'], post['content'], post['author'], post['author'], post['date'], post['image'])
                posts.append(postc)
            
            return render_template('home.html', posts=posts), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']

        try:
            user = auth.sign_in_with_email_and_password(mail, password)
            msg = Message('Logged in successfully!', 'success')
            user = 
            return render_template('home.html', msg=msg, logged=True, user=)
        except Exception as error:
            msg = Message('User not found', 'warning')
            return render_template('auth/login.html', msg=msg)
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        username = request.form['username']
        mail = request.form['mail']
        password = request.form['password']

        if len(username) < 5:
            msg = Message('The username should be at least 5 characters', type='warning')
            return render_template('auth/register.html', msg)
        if len(password) < 8:
            msg = Message('The password should be at least 5 characters', type='warning')
            return render_template('auth/register.html', msg)  

        try:
            user = auth.create_user_with_email_and_password(mail, password)
            json = {'id': mail, 'mail': mail, 'username': username}
            try:
                id = json['id']
                users_ref.document(id).set(json)
                user = User(username, mail)
                msg = Message('Logged in successfully!', 'success')
                return render_template('home.html', msg=msg, logged=True, user=user)
            except Exception as e:
                msg = Message(e, 'error')
                return render_template('auth/register.html', msg=msg)
                
        except Exception as e:
            msg = Message(e, 'error')
            return render_template('home.html', msg=msg)
        
    return render_template('auth/register.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    
    if request.method == "POST":
        title: str = request.form['title']
        content: str = request.form['content']
        author: str = request.form['author']
        date: str = datetime.now()
        try:
            image: str = request.form['image']
            if image == None or image.strip(' ') == '':
                image = 'https://www.logistec.com/wp-content/uploads/2017/12/placeholder.png'
        except:
            image = 'https://www.logistec.com/wp-content/uploads/2017/12/placeholder.png'
        id = ''.join(random.choice(string.ascii_letters) for _ in range(20))
        
        post = Post(id, title, content, author, date, image)
        json = {'id': post.id, 'title': post.title, 'content': post.content, 'author': post.author, 'date': post.date, 'image': post.image}
        
        try:
            id = json['id']
            posts_ref.document(id).set(json)
            return jsonify({"success": True}), 200
        except Exception as e:
            return f'An error occured: {e}'
        
    return render_template('post.html')

@app.route('/u/<username>')
def user(username):

    return render_template('user/profile.html', user=username)

if __name__ == '__main__':
    app.run(debug=True)
