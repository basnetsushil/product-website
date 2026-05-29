import os
import uuid
import csv
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from PIL import Image

from models import db, AdminUser, Enquiry, Article, Event, Testimonial, Solution, TeamMember, SiteSettings
from forms import (ContactForm, AdminLoginForm, EventForm, ArticleForm, 
                   TestimonialForm, SolutionForm, TeamMemberForm, SiteSettingsForm, AdminProfileForm)

# ==========================================
# CONFIGURATION
# ==========================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_solutions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB Limit
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USER', 'your-email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS', 'your-app-password')

# Initialize Extensions
db.init_app(app)
csrf = CSRFProtect(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return AdminUser.query.get(int(user_id))

# ==========================================
# CONTEXT PROCESSORS (Fixes 'datetime is undefined' error)
# ==========================================
@app.context_processor
def inject_now():
    return {'datetime': datetime}

# ==========================================
# IMAGE UPLOAD SYSTEM (Pillow Implementation)
# ==========================================
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file, subfolder, max_width=1200):
    if not file or not allowed_file(file.filename):
        return None
    
    target_dir = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(target_dir, exist_ok=True)
    
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(target_dir, filename)
    
    try:
        img = Image.open(file)
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * float(ratio))
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        img.save(filepath, optimize=True, quality=85)
        return f"uploads/{subfolder}/{filename}"
    except Exception as e:
        print(f"Image processing error: {e}")
        return None

# Initialize Folders and DB
with app.app_context():
    folders = ['events', 'articles', 'testimonials', 'solutions', 'team', 'logo']
    for folder in folders:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder), exist_ok=True)
    db.create_all()

# ==========================================
# PUBLIC ROUTES
# ==========================================

@app.route('/')
def index():
    articles = Article.query.filter_by(is_published=True).order_by(Article.published_at.desc()).limit(3).all()
    testimonials = Testimonial.query.filter_by(is_published=True).limit(3).all()
    solutions = Solution.query.filter_by(is_published=True).order_by(Solution.order_index).limit(3).all()
    settings = SiteSettings.query.first()
    return render_template('index.html', articles=articles, testimonials=testimonials, solutions=solutions, settings=settings)

@app.route('/solutions')
def solutions():
    all_solutions = Solution.query.filter_by(is_published=True).order_by(Solution.order_index).all()
    return render_template('solutions.html', solutions=all_solutions)

@app.route('/case-studies')
def case_studies():
    cases = Article.query.filter_by(category='Case Study', is_published=True).all()
    return render_template('case_studies.html', cases=cases)

@app.route('/testimonials')
def testimonials():
    all_testimonials = Testimonial.query.filter_by(is_published=True).all()
    return render_template('testimonials.html', testimonials=all_testimonials)

@app.route('/articles')
def articles():
    all_articles = Article.query.filter_by(is_published=True).order_by(Article.published_at.desc()).all()
    return render_template('articles.html', articles=all_articles)

@app.route('/articles/<int:id>')
def article_detail(id):
    article = Article.query.get_or_404(id)
    related = Article.query.filter(Article.category == article.category, Article.id != id).limit(3).all()
    return render_template('article_detail.html', article=article, related=related)

@app.route('/events')
def events():
    upcoming = Event.query.filter_by(is_upcoming=True).order_by(Event.event_date.asc()).all()
    past = Event.query.filter_by(is_upcoming=False).order_by(Event.event_date.desc()).all()
    return render_template('events.html', upcoming=upcoming, past=past)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        enquiry = Enquiry(
            name=form.name.data, email=form.email.data, phone=form.phone.data,
            company=form.company.data, country=form.country.data, 
            job_title=form.job_title.data, job_details=form.job_details.data
        )
        db.session.add(enquiry)
        db.session.commit()
        
        try:
            msg = Message("New Website Enquiry", sender=app.config['MAIL_USERNAME'], recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"New enquiry from {form.name.data} ({form.email.data}):\n\n{form.job_details.data}"
            mail.send(msg)
        except:
            pass 
            
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

# ==========================================
# ADMIN AUTH ROUTES
# ==========================================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

# ==========================================
# ADMIN CMS ROUTES
# ==========================================

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    stats = {
        'total_enquiries': Enquiry.query.count(),
        'this_month': Enquiry.query.filter(Enquiry.submitted_at >= datetime(datetime.now().year, datetime.now().month, 1)).count(),
        'total_articles': Article.query.count(),
        'total_events': Event.query.count(),
        'total_team': TeamMember.query.count()
    }
    recent_enquiries = Enquiry.query.order_by(Enquiry.submitted_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, enquiries=recent_enquiries)

@app.route('/admin/enquiry/<int:id>')
@login_required
def enquiry_detail(id):
    enquiry = Enquiry.query.get_or_404(id)
    return render_template('admin/enquiry_detail.html', enquiry=enquiry)

@app.route('/admin/export_enquiries')
@login_required
def export_enquiries():
    enquiries = Enquiry.query.all()
    output = 'enquiries_export.csv'
    with open(output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Company', 'Country', 'Submitted At'])
        for e in enquiries:
            writer.writerow([e.id, e.name, e.email, e.phone, e.company, e.country, e.submitted_at])
    return send_file(output, as_attachment=True)

# --- EVENT MANAGEMENT ---
@app.route('/admin/manage_events')
@login_required
def manage_events():
    events = Event.query.all()
    return render_template('admin/manage_events.html', events=events)

@app.route('/admin/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        img_path = save_image(form.image.data, 'events')
        event = Event(
            name=form.name.data, description=form.description.data,
            event_date=datetime.strptime(form.event_date.data, '%Y-%m-%d'),
            location=form.location.data, image=img_path,
            is_upcoming=form.is_upcoming.data, register_link=form.register_link.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('manage_events'))
    return render_template('admin/add_event.html', form=form)

@app.route('/admin/edit_event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        if form.image.data:
            if event.image:
                try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], event.image))
                except: pass
            event.image = save_image(form.image.data, 'events')
        event.name = form.name.data
        event.description = form.description.data
        event.event_date = datetime.strptime(form.event_date.data, '%Y-%m-%d')
        event.location = form.location.data
        event.is_upcoming = form.is_upcoming.data
        event.register_link = form.register_link.data
        db.session.commit()
        flash('Event updated!', 'success')
        return redirect(url_for('manage_events'))
    return render_template('admin/edit_event.html', form=form, event=event)

@app.route('/admin/delete_event/<int:id>')
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    if event.image:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], event.image))
        except: pass
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted!', 'info')
    return redirect(url_for('manage_events'))

# --- ARTICLE MANAGEMENT ---
@app.route('/admin/manage_articles')
@login_required
def manage_articles():
    articles = Article.query.all()
    return render_template('admin/manage_articles.html', articles=articles)

@app.route('/admin/add_article', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        img_path = save_image(form.cover_image.data, 'articles')
        article = Article(
            title=form.title.data, excerpt=form.excerpt.data, body=form.body.data,
            category=form.category.data, cover_image=img_path,
            author=form.author.data, is_published=form.is_published.data
        )
        db.session.add(article)
        db.session.commit()
        flash('Article added!', 'success')
        return redirect(url_for('manage_articles'))
    return render_template('admin/add_article.html', form=form)

@app.route('/admin/edit_article/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.get_or_404(id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        if form.cover_image.data:
            if article.cover_image:
                try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], article.cover_image))
                except: pass
            article.cover_image = save_image(form.cover_image.data, 'articles')
        article.title = form.title.data
        article.excerpt = form.excerpt.data
        article.body = form.body.data
        article.category = form.category.data
        article.author = form.author.data
        article.is_published = form.is_published.data
        db.session.commit()
        flash('Article updated!', 'success')
        return redirect(url_for('manage_articles'))
    return render_template('admin/edit_article.html', form=form, article=article)

@app.route('/admin/delete_article/<int:id>')
@login_required
def delete_article(id):
    article = Article.query.get_or_404(id)
    if article.cover_image:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], article.cover_image))
        except: pass
    db.session.delete(article)
    db.session.commit()
    flash('Article deleted!', 'info')
    return redirect(url_for('manage_articles'))

# --- TESTIMONIAL MANAGEMENT ---
@app.route('/admin/manage_testimonials')
@login_required
def manage_testimonials():
    testimonials = Testimonial.query.all()
    return render_template('admin/manage_testimonials.html', testimonials=testimonials)

@app.route('/admin/add_testimonial', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        img_path = save_image(form.avatar.data, 'testimonials')
        testimonial = Testimonial(
            customer_name=form.customer_name.data, job_title=form.job_title.data,
            company=form.company.data, quote=form.quote.data,
            rating=form.rating.data, avatar=img_path, is_published=form.is_published.data
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial added!', 'success')
        return redirect(url_for('manage_testimonials'))
    return render_template('admin/add_testimonial.html', form=form)

@app.route('/admin/edit_testimonial/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    form = TestimonialForm(obj=t)
    if form.validate_on_submit():
        if form.avatar.data:
            if t.avatar:
                try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], t.avatar))
                except: pass
            t.avatar = save_image(form.avatar.data, 'testimonials')
        t.customer_name = form.customer_name.data
        t.job_title = form.job_title.data
        t.company = form.company.data
        t.quote = form.quote.data
        t.rating = form.rating.data
        t.is_published = form.is_published.data
        db.session.commit()
        flash('Testimonial updated!', 'success')
        return redirect(url_for('manage_testimonials'))
    return render_template('admin/edit_testimonial.html', form=form, testimonial=t)

@app.route('/admin/delete_testimonial/<int:id>')
@login_required
def delete_testimonial(id):
    t = Testimonial.query.get_or_404(id)
    if t.avatar:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], t.avatar))
        except: pass
    db.session.delete(t)
    db.session.commit()
    flash('Testimonial deleted!', 'info')
    return redirect(url_for('manage_testimonials'))

# --- SOLUTION MANAGEMENT ---
@app.route('/admin/manage_solutions')
@login_required
def manage_solutions():
    solutions = Solution.query.all()
    return render_template('admin/manage_solutions.html', solutions=solutions)

@app.route('/admin/add_solution', methods=['GET', 'POST'])
@login_required
def add_solution():
    form = SolutionForm()
    if form.validate_on_submit():
        img_path = save_image(form.image.data, 'solutions')
        solution = Solution(
            title=form.title.data, description=form.description.data,
            icon_class=form.icon_class.data, image=img_path,
            benefit_1=form.benefit_1.data, benefit_2=form.benefit_2.data,
            benefit_3=form.benefit_3.data, anchor_id=form.anchor_id.data,
            order_index=form.order_index.data, is_published=form.is_published.data
        )
        db.session.add(solution)
        db.session.commit()
        flash('Solution added!', 'success')
        return redirect(url_for('manage_solutions'))
    return render_template('admin/add_solution.html', form=form)

@app.route('/admin/edit_solution/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_solution(id):
    sol = Solution.query.get_or_404(id)
    form = SolutionForm(obj=sol)
    if form.validate_on_submit():
        if form.image.data:
            if sol.image:
                try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], sol.image))
                except: pass
            sol.image = save_image(form.image.data, 'solutions')
        sol.title = form.title.data
        sol.description = form.description.data
        sol.icon_class = form.icon_class.data
        sol.benefit_1 = form.benefit_1.data
        sol.benefit_2 = form.benefit_2.data
        sol.benefit_3 = form.benefit_3.data
        sol.anchor_id = form.anchor_id.data
        sol.order_index = form.order_index.data
        sol.is_published = form.is_published.data
        db.session.commit()
        flash('Solution updated!', 'success')
        return redirect(url_for('manage_solutions'))
    return render_template('admin/edit_solution.html', form=form, solution=sol)

@app.route('/admin/delete_solution/<int:id>')
@login_required
def delete_solution(id):
    sol = Solution.query.get_or_404(id)
    if sol.image:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], sol.image))
        except: pass
    db.session.delete(sol)
    db.session.commit()
    flash('Solution deleted!', 'info')
    return redirect(url_for('manage_solutions'))

# --- TEAM MANAGEMENT ---
@app.route('/admin/manage_team')
@login_required
def manage_team():
    team = TeamMember.query.all()
    return render_template('admin/manage_team.html', team=team)

@app.route('/admin/add_team_member', methods=['GET', 'POST'])
@login_required
def add_team_member():
    form = TeamMemberForm()
    if form.validate_on_submit():
        img_path = save_image(form.photo.data, 'team')
        member = TeamMember(
            name=form.name.data, job_title=form.job_title.data,
            bio=form.bio.data, photo=img_path,
            linkedin_url=form.linkedin_url.data, order_index=form.order_index.data,
            is_published=form.is_published.data
        )
        db.session.add(member)
        db.session.commit()
        flash('Team member added!', 'success')
        return redirect(url_for('manage_team'))
    return render_template('admin/add_team_member.html', form=form)

@app.route('/admin/edit_team_member/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team_member(id):
    m = TeamMember.query.get_or_404(id)
    form = TeamMemberForm(obj=m)
    if form.validate_on_submit():
        if form.photo.data:
            if m.photo:
                try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], m.photo))
                except: pass
            m.photo = save_image(form.photo.data, 'team')
        m.name = form.name.data
        m.job_title = form.job_title.data
        m.bio = form.bio.data
        m.linkedin_url = form.linkedin_url.data
        m.order_index = form.order_index.data
        m.is_published = form.is_published.data
        db.session.commit()
        flash('Team member updated!', 'success')
        return redirect(url_for('manage_team'))
    return render_template('admin/edit_team_member.html', form=form, member=m)

@app.route('/admin/delete_team_member/<int:id>')
@login_required
def delete_team_member(id):
    m = TeamMember.query.get_or_404(id)
    if m.photo:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER'], m.photo))
        except: pass
    db.session.delete(m)
    db.session.commit()
    flash('Team member deleted!', 'info')
    return redirect(url_for('manage_team'))

# --- SETTINGS MANAGEMENT ---
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings_obj = SiteSettings.query.first()
    if not settings_obj:
        settings_obj = SiteSettings()
        db.session.add(settings_obj)
        db.session.commit()
    
    form = SiteSettingsForm(obj=settings_obj)
    if form.validate_on_submit():
        if form.company_logo.data:
            img_path = save_image(form.company_logo.data, 'logo')
            settings_obj.company_logo = img_path
        
        settings_obj.company_name = form.company_name.data
        settings_obj.tagline = form.tagline.data
        settings_obj.address = form.address.data
        settings_obj.email = form.email.data
        settings_obj.phone = form.phone.data
        settings_obj.linkedin_url = form.linkedin_url.data
        settings_obj.twitter_url = form.twitter_url.data
        settings_obj.facebook_url = form.facebook_url.data
        settings_obj.instagram_url = form.instagram_url.data
        settings_obj.github_url = form.github_url.data
        db.session.commit()
        flash('Settings updated!', 'success')
    return render_template('admin/settings.html', form=form, settings=settings_obj)

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)