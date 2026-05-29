from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class AdminUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255), default='default_admin.jpg')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    country = db.Column(db.String(50))
    job_title = db.Column(db.String(100))
    job_details = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.String(500))
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    cover_image = db.Column(db.String(255))
    author = db.Column(db.String(100))
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
    image = db.Column(db.String(255))
    is_upcoming = db.Column(db.Boolean, default=True)
    register_link = db.Column(db.String(255))

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    quote = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    avatar = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=True)

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon_class = db.Column(db.String(50)) # Tailwind/Lucide class
    image = db.Column(db.String(255))
    benefit_1 = db.Column(db.String(255))
    benefit_2 = db.Column(db.String(255))
    benefit_3 = db.Column(db.String(255))
    anchor_id = db.Column(db.String(50))
    order_index = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)

class CaseStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    client_name = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    challenge = db.Column(db.Text)
    solution_used = db.Column(db.Text)
    result = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=True)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100))
    bio = db.Column(db.Text)
    photo = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    order_index = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_logo = db.Column(db.String(255))
    company_name = db.Column(db.String(100), default="AI-Solutions")
    tagline = db.Column(db.String(255))
    address = db.Column(db.String(255))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    linkedin_url = db.Column(db.String(255))
    twitter_url = db.Column(db.String(255))
    facebook_url = db.Column(db.String(255))
    instagram_url = db.Column(db.String(255))
    github_url = db.Column(db.String(255))