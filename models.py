from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_picture = db.Column(db.String(300), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Enquiry(db.Model):
    __tablename__ = 'enquiry'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50))
    company = db.Column(db.String(100))
    country = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    job_details = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.String(500))
    body = db.Column(db.Text)
    category = db.Column(db.String(100))
    cover_image = db.Column(db.String(300), nullable=True)
    author = db.Column(db.String(100), default='AI-Solutions Team')
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    image = db.Column(db.String(300), nullable=True)
    is_upcoming = db.Column(db.Boolean, default=False)
    register_link = db.Column(db.String(300), nullable=True)

class Testimonial(db.Model):
    __tablename__ = 'testimonial'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    quote = db.Column(db.Text)
    rating = db.Column(db.Integer, default=5)
    avatar = db.Column(db.String(300), nullable=True)
    is_published = db.Column(db.Boolean, default=True)

class Solution(db.Model):
    __tablename__ = 'solution'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon_class = db.Column(db.String(100), default='fas fa-robot')
    image = db.Column(db.String(300), nullable=True)
    benefit_1 = db.Column(db.String(200))
    benefit_2 = db.Column(db.String(200))
    benefit_3 = db.Column(db.String(200))
    anchor_id = db.Column(db.String(100))
    order_index = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)

class TeamMember(db.Model):
    __tablename__ = 'team_member'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100))
    bio = db.Column(db.Text)
    photo = db.Column(db.String(300), nullable=True)
    linkedin_url = db.Column(db.String(300), nullable=True)
    order_index = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(100), default='General')
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    company_logo = db.Column(db.String(300), nullable=True)
    company_name = db.Column(db.String(200), default='AI-Solutions')
    tagline = db.Column(db.String(500))
    address = db.Column(db.String(300))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    linkedin_url = db.Column(db.String(300), nullable=True)
    twitter_url = db.Column(db.String(300), nullable=True)
    facebook_url = db.Column(db.String(300), nullable=True)
    instagram_url = db.Column(db.String(300), nullable=True)
    github_url = db.Column(db.String(300), nullable=True)