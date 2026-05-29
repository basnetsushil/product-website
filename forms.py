from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, PasswordField, IntegerField, FileField, SubmitField 
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from flask_wtf.file import FileAllowed

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    company = StringField('Company', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    job_title = StringField('Job Title', validators=[Optional()])
    job_details = TextAreaField('How can we help?', validators=[DataRequired(), Length(min=10)])

from wtforms import StringField, TextAreaField, BooleanField, PasswordField, IntegerField, FileField # Ensure BooleanField is imported!

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') # <--- ADD THIS LINE

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    image = FileField('Event Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    is_upcoming = BooleanField('Is Upcoming?')
    register_link = StringField('Registration Link', validators=[Optional()])

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    excerpt = StringField('Excerpt', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    cover_image = FileField('Cover Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    author = StringField('Author', validators=[DataRequired()])
    is_published = BooleanField('Published?')

class TestimonialForm(FlaskForm):
    customer_name = StringField('Name', validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[Optional()])
    company = StringField('Company', validators=[Optional()])
    quote = TextAreaField('Quote', validators=[DataRequired()])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired()])
    avatar = FileField('Avatar', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    is_published = BooleanField('Published?')

class SolutionForm(FlaskForm):
    title = StringField('Solution Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    icon_class = StringField('Icon Class (e.g. lucide-cpu)', validators=[Optional()])
    image = FileField('Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    benefit_1 = StringField('Benefit 1', validators=[DataRequired()])
    benefit_2 = StringField('Benefit 2', validators=[DataRequired()])
    benefit_3 = StringField('Benefit 3', validators=[DataRequired()])
    anchor_id = StringField('Anchor ID (for scrolling)', validators=[Optional()])
    order_index = IntegerField('Display Order', default=0)
    is_published = BooleanField('Published?')

class TeamMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    photo = FileField('Photo', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional()])
    order_index = IntegerField('Order Index', default=0)
    is_published = BooleanField('Published?')

class SiteSettingsForm(FlaskForm):
    company_logo = FileField('Logo', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    company_name = StringField('Company Name', validators=[DataRequired()])
    tagline = StringField('Tagline', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    email = StringField('Contact Email', validators=[DataRequired(), Email()])
    phone = StringField('Contact Phone', validators=[DataRequired()])
    linkedin_url = StringField('LinkedIn', validators=[Optional()])
    twitter_url = StringField('Twitter', validators=[Optional()])
    facebook_url = StringField('Facebook', validators=[Optional()])
    instagram_url = StringField('Instagram', validators=[Optional()])
    github_url = StringField('GitHub', validators=[Optional()])

class AdminProfileForm(FlaskForm):
    profile_picture = FileField('Profile Picture', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])