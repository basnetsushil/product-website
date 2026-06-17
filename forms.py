from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, TextAreaField, BooleanField, PasswordField,
                     SelectField, IntegerField, SubmitField, DateTimeLocalField)
from wtforms.validators import DataRequired, Email, Optional, EqualTo, Length, NumberRange, URL

COUNTRIES = [
    ('','Select Country'), ('Afghanistan','Afghanistan'),('Albania','Albania'),('Algeria','Algeria'),
    ('Andorra','Andorra'),('Angola','Angola'),('Argentina','Argentina'),('Armenia','Armenia'),
    ('Australia','Australia'),('Austria','Austria'),('Azerbaijan','Azerbaijan'),('Bahamas','Bahamas'),
    ('Bahrain','Bahrain'),('Bangladesh','Bangladesh'),('Belarus','Belarus'),('Belgium','Belgium'),
    ('Belize','Belize'),('Benin','Benin'),('Bhutan','Bhutan'),('Bolivia','Bolivia'),
    ('Bosnia and Herzegovina','Bosnia and Herzegovina'),('Botswana','Botswana'),('Brazil','Brazil'),
    ('Brunei','Brunei'),('Bulgaria','Bulgaria'),('Burkina Faso','Burkina Faso'),('Burundi','Burundi'),
    ('Cambodia','Cambodia'),('Cameroon','Cameroon'),('Canada','Canada'),('Chad','Chad'),('Chile','Chile'),
    ('China','China'),('Colombia','Colombia'),('Congo','Congo'),('Costa Rica','Costa Rica'),
    ('Croatia','Croatia'),('Cuba','Cuba'),('Cyprus','Cyprus'),('Czech Republic','Czech Republic'),
    ('Denmark','Denmark'),('Ecuador','Ecuador'),('Egypt','Egypt'),('El Salvador','El Salvador'),
    ('Estonia','Estonia'),('Ethiopia','Ethiopia'),('Finland','Finland'),('France','France'),
    ('Georgia','Georgia'),('Germany','Germany'),('Ghana','Ghana'),('Greece','Greece'),
    ('Guatemala','Guatemala'),('Honduras','Honduras'),('Hungary','Hungary'),('Iceland','Iceland'),
    ('India','India'),('Indonesia','Indonesia'),('Iran','Iran'),('Iraq','Iraq'),('Ireland','Ireland'),
    ('Israel','Israel'),('Italy','Italy'),('Jamaica','Jamaica'),('Japan','Japan'),('Jordan','Jordan'),
    ('Kazakhstan','Kazakhstan'),('Kenya','Kenya'),('Kuwait','Kuwait'),('Latvia','Latvia'),
    ('Lebanon','Lebanon'),('Libya','Libya'),('Lithuania','Lithuania'),('Luxembourg','Luxembourg'),
    ('Malaysia','Malaysia'),('Maldives','Maldives'),('Mali','Mali'),('Malta','Malta'),('Mexico','Mexico'),
    ('Moldova','Moldova'),('Monaco','Monaco'),('Mongolia','Mongolia'),('Montenegro','Montenegro'),
    ('Morocco','Morocco'),('Mozambique','Mozambique'),('Myanmar','Myanmar'),('Namibia','Namibia'),
    ('Nepal','Nepal'),('Netherlands','Netherlands'),('New Zealand','New Zealand'),('Nicaragua','Nicaragua'),
    ('Niger','Niger'),('Nigeria','Nigeria'),('Norway','Norway'),('Oman','Oman'),('Pakistan','Pakistan'),
    ('Panama','Panama'),('Paraguay','Paraguay'),('Peru','Peru'),('Philippines','Philippines'),
    ('Poland','Poland'),('Portugal','Portugal'),('Qatar','Qatar'),('Romania','Romania'),
    ('Russia','Russia'),('Rwanda','Rwanda'),('Saudi Arabia','Saudi Arabia'),('Senegal','Senegal'),
    ('Serbia','Serbia'),('Singapore','Singapore'),('Slovakia','Slovakia'),('Slovenia','Slovenia'),
    ('Somalia','Somalia'),('South Africa','South Africa'),('South Korea','South Korea'),
    ('Spain','Spain'),('Sri Lanka','Sri Lanka'),('Sudan','Sudan'),('Sweden','Sweden'),
    ('Switzerland','Switzerland'),('Syria','Syria'),('Taiwan','Taiwan'),('Tanzania','Tanzania'),
    ('Thailand','Thailand'),('Tunisia','Tunisia'),('Turkey','Turkey'),('Uganda','Uganda'),
    ('Ukraine','Ukraine'),('United Arab Emirates','United Arab Emirates'),
    ('United Kingdom','United Kingdom'),('United States','United States'),('Uruguay','Uruguay'),
    ('Uzbekistan','Uzbekistan'),('Venezuela','Venezuela'),('Vietnam','Vietnam'),('Yemen','Yemen'),
    ('Zambia','Zambia'),('Zimbabwe','Zimbabwe'),
]

ALLOWED = ['jpg','jpeg','png','gif','webp']

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=50)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    country = SelectField('Country', choices=COUNTRIES, validators=[Optional()])
    job_title = StringField('Job Title', validators=[Optional(), Length(max=100)])
    job_details = TextAreaField('Tell us about your project', validators=[DataRequired()])
    submit = SubmitField('Send Enquiry')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = DateTimeLocalField('Event Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=200)])
    image = FileField('Event Image', validators=[Optional(), FileAllowed(ALLOWED, 'Images only!')])
    is_upcoming = BooleanField('Mark as Upcoming')
    register_link = StringField('Registration Link', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Save Event')

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    excerpt = StringField('Excerpt', validators=[Optional(), Length(max=500)])
    body = TextAreaField('Body', validators=[DataRequired()])
    category = StringField('Category', validators=[Optional(), Length(max=100)])
    cover_image = FileField('Cover Image', validators=[Optional(), FileAllowed(ALLOWED, 'Images only!')])
    author = StringField('Author', validators=[Optional(), Length(max=100)])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save Article')

class TestimonialForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=100)])
    job_title = StringField('Job Title', validators=[Optional(), Length(max=100)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])
    quote = TextAreaField('Quote', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[(1,'1 Star'),(2,'2 Stars'),(3,'3 Stars'),(4,'4 Stars'),(5,'5 Stars')], coerce=int)
    avatar = FileField('Avatar', validators=[Optional(), FileAllowed(ALLOWED, 'Images only!')])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save Testimonial')

class SolutionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    icon_class = StringField('Icon Class', validators=[Optional(), Length(max=100)])
    image = FileField('Solution Image', validators=[Optional(), FileAllowed(ALLOWED, 'Images only!')])
    benefit_1 = StringField('Benefit 1', validators=[Optional(), Length(max=200)])
    benefit_2 = StringField('Benefit 2', validators=[Optional(), Length(max=200)])
    benefit_3 = StringField('Benefit 3', validators=[Optional(), Length(max=200)])
    anchor_id = StringField('Anchor ID', validators=[Optional(), Length(max=100)])
    order_index = IntegerField('Order', default=0, validators=[Optional()])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save Solution')

class TeamMemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    job_title = StringField('Job Title', validators=[Optional(), Length(max=100)])
    bio = TextAreaField('Bio', validators=[Optional()])
    photo = FileField('Photo', validators=[Optional(), FileAllowed(ALLOWED, 'Images only!')])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), Length(max=300)])
    order_index = IntegerField('Order', default=0, validators=[Optional()])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save Team Member')

class SiteSettingsForm(FlaskForm):
    company_logo = FileField('Company Logo', validators=[Optional(), FileAllowed(ALLOWED, 'Images only!')])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=200)])
    tagline = StringField('Tagline', validators=[Optional(), Length(max=500)])
    address = StringField('Address', validators=[Optional(), Length(max=300)])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=50)])
    linkedin_url = StringField('LinkedIn', validators=[Optional(), Length(max=300)])
    twitter_url = StringField('Twitter/X', validators=[Optional(), Length(max=300)])
    facebook_url = StringField('Facebook', validators=[Optional(), Length(max=300)])
    instagram_url = StringField('Instagram', validators=[Optional(), Length(max=300)])
    github_url = StringField('GitHub', validators=[Optional(), Length(max=300)])
    submit = SubmitField('Save Settings')

class GalleryForm(FlaskForm):
    title = StringField('Image Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    category = StringField('Category', validators=[Optional(), Length(max=100)])
    image = FileField('Gallery Image', validators=[DataRequired(), FileAllowed(ALLOWED, 'Images only!')])
    order_index = IntegerField('Order', default=0, validators=[Optional()])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save Gallery Image')

class AdminProfileForm(FlaskForm):
    profile_picture = FileField('Profile Picture', validators=[Optional(), FileAllowed(ALLOWED, 'Images only!')])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[Optional(), EqualTo('new_password', message='Passwords must match')])
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    submit = SubmitField('Update Profile')