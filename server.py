from flask import Flask, request, jsonify,send_from_directory, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configurations from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
db = SQLAlchemy(app)
jwt = JWTManager(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

# Project model
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(80), nullable=True)
    github = db.Column(db.String(80), nullable=True)
    img = db.Column(db.String(80), nullable=False)

    def __init__(self, title, description, link=None, github=None, img=None):
        self.title = title
        self.description = description
        self.link = link
        self.github = github
        self.img = img

# Create tables
with app.app_context():
    db.create_all()
# Custom behavior when JWT is missing or invalid

#@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # Redirect to the index page if JWT is missing
    return redirect(url_for('index'))

#@jwt.invalid_token_loader
def invalid_token_callback(callback):
    # Redirect to the index page if JWT is invalid
    return redirect(url_for('index'))

#@jwt.expired_token_loader
def expired_token_callback(callback, callback2):
    # Redirect to the index page if JWT has expired
    return redirect(url_for('index'))


# Register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400
    
    new_user = User(username, password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)

    # Set JWT token in a cookie
    response = jsonify({"message": "Login successful"})
    set_access_cookies(response, access_token)
    
    return response, 200

# Protected route for viewing the dashboard (JWT required)
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    projects = Projects.query.all()
    return render_template('dashboard.html', projects=projects)

# Add a new project (JWT required)
# Add a new project (JWT required)
@app.route('/add_project', methods=['POST'])
@jwt_required()
def add_project():
    print(request.files)
    title = request.form['title']
    description = request.form['description']
    link = request.form.get('link')
    github = request.form.get('github')
    image = request.files.get('image')

    image_filename = secure_filename(image.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    print(f'Saving image to: {save_path}')  # Debugging print statement
    image.save(save_path)

    new_project = Projects(title=title, description=description, link=link, github=github, img=image_filename)

    db.session.add(new_project)
    db.session.commit()

    return jsonify({"message": "Project added successfully!"}), 200

# Delete a project (JWT required)
@app.route('/delete_project/<int:id>', methods=['POST'])
@jwt_required()
def delete_project(id):
    project = Projects.query.get(id)
    if project:
        db.session.delete(project)
        db.session.commit()
    
    return redirect(url_for('dashboard'))

# Render login page
@app.route('/login', methods=['GET'])
def loginPage():
    return render_template('login.html')
@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API endpoint to get projects data (JWT required)
@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Projects.query.all()
    projects_list = [
        {
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'link': project.link,
            'github': project.github,
            'img': project.img
        }
        for project in projects
    ]

    return jsonify(projects_list), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
