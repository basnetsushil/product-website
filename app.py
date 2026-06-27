import os
import csv
import uuid
import socket
from io import StringIO
from datetime import datetime, timedelta
from functools import wraps

from flask import (Flask, render_template, redirect, url_for, flash, request,
                   send_file, make_response, g)
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from sqlalchemy import desc, func, or_
from werkzeug.utils import secure_filename
from PIL import Image as PILImage

from models import db, AdminUser, Enquiry, Article, Event, Testimonial, Solution, TeamMember, SiteSettings, Gallery
from forms import (ContactForm, AdminLoginForm, EventForm, ArticleForm, TestimonialForm,
                   SolutionForm, TeamMemberForm, SiteSettingsForm, AdminProfileForm, GalleryForm)

from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod-2024')
database_url = os.environ.get('DATABASE_URL', 'sqlite:///ai_solutions.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 25))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'info@ai-solutions.uk')
app.config['MAIL_SUPPRESS_SEND'] = not bool(app.config['MAIL_SERVER'])
app.config['MAIL_TIMEOUT'] = int(os.environ.get('MAIL_TIMEOUT', 5))
app.config['MAIL_RECIPIENTS'] = [
    email.strip()
    for email in os.environ.get('MAIL_RECIPIENTS', app.config['MAIL_DEFAULT_SENDER']).split(',')
    if email.strip()
]

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(app.instance_path, exist_ok=True)

csrf = CSRFProtect(app)
db.init_app(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'error'

# Create upload folders
for folder in ['events', 'articles', 'testimonials', 'solutions', 'team', 'logo', 'admin', 'gallery']:
    os.makedirs(os.path.join('static/uploads', folder), exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(AdminUser, int(user_id))


# ── Helpers ────────────────────────────────────────────────────────────────────

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file, subfolder, max_width=1200):
    try:
        if not file or not allowed_file(file.filename):
            return None
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        save_dir = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(save_dir, exist_ok=True)
        filepath = os.path.join(save_dir, filename)
        file.save(filepath)
        try:
            img = PILImage.open(filepath)
            if img.width > max_width:
                ratio = max_width / img.width
                new_h = int(img.height * ratio)
                img = img.resize((max_width, new_h), PILImage.LANCZOS)
                img.save(filepath)
        except Exception:
            pass
        return f"uploads/{subfolder}/{filename}"
    except Exception as e:
        print(f"Image save error: {e}")
        return None


def delete_image(path):
    if path:
        full = os.path.join('static', path)
        if os.path.exists(full):
            try:
                os.remove(full)
            except Exception:
                pass


def send_enquiry_notification(form):
    if app.config['MAIL_SUPPRESS_SEND'] or not app.config['MAIL_RECIPIENTS']:
        app.logger.info('Skipping enquiry email because MAIL_SERVER is not configured.')
        return

    msg = Message(
        subject=f"New Enquiry from {form.name.data}",
        recipients=app.config['MAIL_RECIPIENTS'],
        body=(
            f"Name: {form.name.data}\n"
            f"Email: {form.email.data}\n"
            f"Phone: {form.phone.data or 'Not provided'}\n"
            f"Company: {form.company.data or 'Not provided'}\n"
            f"Country: {form.country.data or 'Not provided'}\n"
            f"Job Title: {form.job_title.data or 'Not provided'}\n\n"
            f"{form.job_details.data}"
        )
    )

    previous_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(app.config['MAIL_TIMEOUT'])
    try:
        mail.send(msg)
    except Exception:
        app.logger.exception('Failed to send enquiry notification email.')
    finally:
        socket.setdefaulttimeout(previous_timeout)


def init_database():
    with app.app_context():
        db.create_all()
        if not db.session.get(SiteSettings, 1):
            db.session.add(SiteSettings(
                id=1,
                company_name='AI-Solutions',
                email='info@ai-solutions.uk',
                phone='+44 (0)191 123 4567',
                address='Sunderland, UK'
            ))
            db.session.commit()


@app.context_processor
def inject_settings():
    try:
        settings = db.session.get(SiteSettings, 1)
    except Exception:
        db.session.rollback()
        settings = None
        app.logger.exception('Could not load site settings.')
    if not settings:
        settings = SiteSettings(id=1, company_name='AI-Solutions')
    return dict(settings=settings)


try:
    init_database()
except Exception:
    app.logger.exception('Database initialization failed during app startup.')


# ── Public Routes ───────────────────────────────────────────────────────────────

@app.route('/')
def index():
    articles = Article.query.filter_by(is_published=True).order_by(desc(Article.published_at)).limit(3).all()
    testimonials = Testimonial.query.filter_by(is_published=True).limit(3).all()
    solutions = Solution.query.filter_by(is_published=True).order_by(Solution.order_index).limit(3).all()
    team = TeamMember.query.filter_by(is_published=True).order_by(TeamMember.order_index).limit(4).all()
    gallery = Gallery.query.filter_by(is_published=True).order_by(Gallery.order_index).limit(6).all()
    return render_template('index.html', articles=articles, testimonials=testimonials,
                           solutions=solutions, team=team, gallery=gallery)


@app.route('/solutions')
def solutions():
    sols = Solution.query.filter_by(is_published=True).order_by(Solution.order_index).all()
    return render_template('solutions.html', solutions=sols)


@app.route('/case-studies')
def case_studies():
    selected_industry = request.args.get('industry', '').strip()
    case_study_items = [
        {
            'number': '01',
            'industry': 'Manufacturing',
            'solution': 'Computer Vision',
            'title': 'Eliminating defects on the production line',
            'stat': '-50%',
            'stat_label': 'defect rate in 6 months',
        },
        {
            'number': '02',
            'industry': 'Retail',
            'solution': 'NLP & Automation',
            'title': 'Transforming customer service at scale',
            'stat': '+18pts',
            'stat_label': 'customer satisfaction score',
        },
        {
            'number': '03',
            'industry': 'Logistics',
            'solution': 'Predictive Analytics',
            'title': 'Demand forecasting that moved the needle',
            'stat': '90 days',
            'stat_label': 'accurate demand visibility',
        },
        {
            'number': '04',
            'industry': 'Healthcare',
            'solution': 'AI Strategy',
            'title': 'Building an AI roadmap for a health trust',
            'stat': '12mo',
            'stat_label': 'from assessment to deployment',
        },
        {
            'number': '05',
            'industry': 'Finance',
            'solution': 'Process Automation',
            'title': 'Automating invoice processing end-to-end',
            'stat': '70%',
            'stat_label': 'reduction in processing time',
        },
    ]
    industries = ['Finance', 'Healthcare', 'Retail', 'Manufacturing', 'Logistics']
    filtered_cases = [
        item for item in case_study_items
        if not selected_industry or item['industry'] == selected_industry
    ]
    return render_template(
        'case_studies.html',
        case_studies=filtered_cases,
        industries=industries,
        selected_industry=selected_industry
    )


@app.route('/testimonials')
def testimonials():
    testimonials = Testimonial.query.filter_by(is_published=True).all()
    return render_template('testimonials.html', testimonials=testimonials)


@app.route('/articles')
def articles():
    selected_category = request.args.get('category', '').strip()
    search_query = request.args.get('q', '').strip()
    category_rows = (
        db.session.query(Article.category)
        .filter(Article.is_published == True, Article.category.isnot(None), Article.category != '')
        .distinct()
        .order_by(Article.category)
        .all()
    )
    categories = [row[0] for row in category_rows]

    article_query = Article.query.filter_by(is_published=True)
    if selected_category:
        article_query = article_query.filter(Article.category == selected_category)
    if search_query:
        like_query = f'%{search_query}%'
        article_query = article_query.filter(or_(
            Article.title.ilike(like_query),
            Article.excerpt.ilike(like_query),
            Article.body.ilike(like_query),
            Article.category.ilike(like_query),
            Article.author.ilike(like_query)
        ))

    articles = article_query.order_by(desc(Article.published_at)).all()
    return render_template(
        'articles.html',
        articles=articles,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query
    )


@app.route('/articles/<int:id>')
def article_detail(id):
    article = db.get_or_404(Article, id)
    related = Article.query.filter(Article.id != id, Article.is_published == True).limit(3).all()
    return render_template('article_detail.html', article=article, related=related)


@app.route('/events')
def events():
    upcoming = Event.query.filter_by(is_upcoming=True).order_by(Event.event_date).all()
    past = Event.query.filter_by(is_upcoming=False).order_by(desc(Event.event_date)).all()
    return render_template('events.html', upcoming=upcoming, past=past)


@app.route('/gallery')
def gallery():
    galleries = Gallery.query.filter_by(is_published=True).order_by(Gallery.order_index).all()
    return render_template('gallery.html', galleries=galleries)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    try:
        site = db.session.get(SiteSettings, 1)
    except Exception:
        db.session.rollback()
        app.logger.exception('Could not load site settings on contact page.')
        site = None
    if form.validate_on_submit():
        try:
            enquiry = Enquiry(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                company=form.company.data,
                country=form.country.data,
                job_title=form.job_title.data,
                job_details=form.job_details.data
            )
            db.session.add(enquiry)
            db.session.commit()
        except Exception:
            db.session.rollback()
            app.logger.exception('Failed to save contact enquiry.')
            flash('Sorry, your enquiry could not be saved right now. Please try again in a moment.', 'error')
            return render_template('contact.html', form=form, site=site), 500

        send_enquiry_notification(form)
        flash('Thank you! Your enquiry has been received. We\'ll be in touch shortly.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form, site=site)


# ── Admin Auth ─────────────────────────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = AdminUser.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('admin/login.html', form=form)


@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin_login'))


# ── Admin Dashboard ────────────────────────────────────────────────────────────

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # 1. Time Logic
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0)

    # 2. Stats Dictionary (Matches HTML exactly)
    stats = {
        'this_month': Enquiry.query.filter(Enquiry.submitted_at >= month_start).count(),
        'total_enquiries': Enquiry.query.count(),
        'total_articles': Article.query.count(),
        'total_events': Event.query.count(),
        'total_team': TeamMember.query.count(),
        'total_case_studies': 0, # Add count logic if you have a CaseStudy model
    }

    # 3. Geographic reach (Matches HTML 'country_data' dictionary)
    country_results = db.session.query(Enquiry.country, func.count(Enquiry.id)).group_by(Enquiry.country).all()
    country_data = {country: count for country, count in country_results if country}

    # 4. Chart Data (Matches HTML 'monthly_data' and 'month_labels')
    monthly_data = []
    month_labels = []
    for i in range(5, -1, -1):
        d = now - timedelta(days=30 * i)
        label = d.strftime('%b') # 'Jan', 'Feb', etc.
        start = d.replace(day=1, hour=0, minute=0, second=0)
        # Calculate end of that specific month
        next_month = (start + timedelta(days=32)).replace(day=1)
        
        cnt = Enquiry.query.filter(Enquiry.submitted_at >= start, Enquiry.submitted_at < next_month).count()
        monthly_data.append(cnt)
        month_labels.append(label)

    # 5. Recent Enquiries (Matches HTML 'enquiries' loop)
    enquiries = Enquiry.query.order_by(desc(Enquiry.submitted_at)).limit(10).all()

    return render_template('admin/dashboard.html',
                           stats=stats, 
                           enquiries=enquiries,
                           country_data=country_data, 
                           monthly_data=monthly_data, 
                           month_labels=month_labels)


# ── Admin Enquiries ────────────────────────────────────────────────────────────

@app.route('/admin/enquiries')
@login_required
def admin_enquiries():
    enquiries = Enquiry.query.order_by(desc(Enquiry.submitted_at)).all()
    return render_template('admin/enquiries.html', enquiries=enquiries)


@app.route('/admin/enquiries/<int:id>')
@login_required
def enquiry_detail(id):
    enquiry = db.get_or_404(Enquiry, id)
    return render_template('admin/enquiry_detail.html', enquiry=enquiry)


@app.route('/admin/enquiries/<int:id>/delete', methods=['POST'])
@login_required
def delete_enquiry(id):
    enquiry = db.get_or_404(Enquiry, id)
    db.session.delete(enquiry)
    db.session.commit()
    flash('Enquiry deleted.', 'success')
    return redirect(url_for('admin_enquiries'))


@app.route('/admin/export')
@login_required
def export_enquiries():
    enquiries = Enquiry.query.order_by(desc(Enquiry.submitted_at)).all()
    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Company', 'Country', 'Job Title', 'Details', 'Date'])
    for e in enquiries:
        writer.writerow([e.id, e.name, e.email, e.phone, e.company, e.country,
                         e.job_title, e.job_details, e.submitted_at])
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = 'attachment; filename=enquiries.csv'
    output.headers['Content-type'] = 'text/csv'
    return output


# ── Admin Events ───────────────────────────────────────────────────────────────

@app.route('/admin/events')
@login_required
def admin_events():
    events = Event.query.order_by(desc(Event.event_date)).all()
    return render_template('admin/manage_events.html', events=events)


@app.route('/admin/events/add', methods=['GET', 'POST'])
@login_required
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        img_path = save_image(form.image.data, 'events') if form.image.data and form.image.data.filename else None
        event = Event(name=form.name.data, description=form.description.data,
                      event_date=form.event_date.data, location=form.location.data,
                      image=img_path, is_upcoming=form.is_upcoming.data,
                      register_link=form.register_link.data)
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('admin_events'))
    return render_template('admin/add_event.html', form=form)


@app.route('/admin/events/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = db.get_or_404(Event, id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        if form.image.data and form.image.data.filename:
            delete_image(event.image)
            event.image = save_image(form.image.data, 'events')
        event.name = form.name.data
        event.description = form.description.data
        event.event_date = form.event_date.data
        event.location = form.location.data
        event.is_upcoming = form.is_upcoming.data
        event.register_link = form.register_link.data
        db.session.commit()
        flash('Event updated!', 'success')
        return redirect(url_for('admin_events'))
    return render_template('admin/edit_event.html', form=form, event=event)


@app.route('/admin/events/<int:id>/delete', methods=['POST'])
@login_required
def delete_event(id):
    event = db.get_or_404(Event, id)
    delete_image(event.image)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'success')
    return redirect(url_for('admin_events'))


# ── Admin Articles ─────────────────────────────────────────────────────────────

@app.route('/admin/articles')
@login_required
def admin_articles():
    articles = Article.query.order_by(desc(Article.published_at)).all()
    return render_template('admin/manage_articles.html', articles=articles)


@app.route('/admin/articles/add', methods=['GET', 'POST'])
@login_required
def add_article():
    form = ArticleForm()
    if form.validate_on_submit():
        img_path = save_image(form.cover_image.data, 'articles') if form.cover_image.data and form.cover_image.data.filename else None
        article = Article(title=form.title.data, excerpt=form.excerpt.data, body=form.body.data,
                          category=form.category.data, cover_image=img_path,
                          author=form.author.data or 'AI-Solutions Team',
                          is_published=form.is_published.data)
        db.session.add(article)
        db.session.commit()
        flash('Article published!', 'success')
        return redirect(url_for('admin_articles'))
    return render_template('admin/add_article.html', form=form)


@app.route('/admin/articles/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = db.get_or_404(Article, id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        if form.cover_image.data and form.cover_image.data.filename:
            delete_image(article.cover_image)
            article.cover_image = save_image(form.cover_image.data, 'articles')
        article.title = form.title.data
        article.excerpt = form.excerpt.data
        article.body = form.body.data
        article.category = form.category.data
        article.author = form.author.data
        article.is_published = form.is_published.data
        db.session.commit()
        flash('Article updated!', 'success')
        return redirect(url_for('admin_articles'))
    return render_template('admin/edit_article.html', form=form, article=article)


@app.route('/admin/articles/<int:id>/delete', methods=['POST'])
@login_required
def delete_article(id):
    article = db.get_or_404(Article, id)
    delete_image(article.cover_image)
    db.session.delete(article)
    db.session.commit()
    flash('Article deleted.', 'success')
    return redirect(url_for('admin_articles'))


# ── Admin Testimonials ─────────────────────────────────────────────────────────

@app.route('/admin/testimonials')
@login_required
def admin_testimonials():
    testimonials = Testimonial.query.all()
    return render_template('admin/manage_testimonials.html', testimonials=testimonials)


@app.route('/admin/testimonials/add', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        img_path = save_image(form.avatar.data, 'testimonials') if form.avatar.data and form.avatar.data.filename else None
        t = Testimonial(customer_name=form.customer_name.data, job_title=form.job_title.data,
                        company=form.company.data, quote=form.quote.data, rating=form.rating.data,
                        avatar=img_path, is_published=form.is_published.data)
        db.session.add(t)
        db.session.commit()
        flash('Testimonial added!', 'success')
        return redirect(url_for('admin_testimonials'))
    return render_template('admin/add_testimonial.html', form=form)


@app.route('/admin/testimonials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonial(id):
    t = db.get_or_404(Testimonial, id)
    form = TestimonialForm(obj=t)
    if form.validate_on_submit():
        if form.avatar.data and form.avatar.data.filename:
            delete_image(t.avatar)
            t.avatar = save_image(form.avatar.data, 'testimonials')
        t.customer_name = form.customer_name.data
        t.job_title = form.job_title.data
        t.company = form.company.data
        t.quote = form.quote.data
        t.rating = form.rating.data
        t.is_published = form.is_published.data
        db.session.commit()
        flash('Testimonial updated!', 'success')
        return redirect(url_for('admin_testimonials'))
    return render_template('admin/edit_testimonial.html', form=form, testimonial=t)


@app.route('/admin/testimonials/<int:id>/delete', methods=['POST'])
@login_required
def delete_testimonial(id):
    t = db.get_or_404(Testimonial, id)
    delete_image(t.avatar)
    db.session.delete(t)
    db.session.commit()
    flash('Testimonial deleted.', 'success')
    return redirect(url_for('admin_testimonials'))


# ── Admin Solutions ────────────────────────────────────────────────────────────

@app.route('/admin/solutions')
@login_required
def admin_solutions():
    solutions = Solution.query.order_by(Solution.order_index).all()
    return render_template('admin/manage_solutions.html', solutions=solutions)


@app.route('/admin/solutions/add', methods=['GET', 'POST'])
@login_required
def add_solution():
    form = SolutionForm()
    if form.validate_on_submit():
        img_path = save_image(form.image.data, 'solutions') if form.image.data and form.image.data.filename else None
        s = Solution(title=form.title.data, description=form.description.data,
                     icon_class=form.icon_class.data, image=img_path,
                     benefit_1=form.benefit_1.data, benefit_2=form.benefit_2.data,
                     benefit_3=form.benefit_3.data, anchor_id=form.anchor_id.data,
                     order_index=form.order_index.data or 0, is_published=form.is_published.data)
        db.session.add(s)
        db.session.commit()
        flash('Solution added!', 'success')
        return redirect(url_for('admin_solutions'))
    return render_template('admin/add_solution.html', form=form)


@app.route('/admin/solutions/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_solution(id):
    s = db.get_or_404(Solution, id)
    form = SolutionForm(obj=s)
    if form.validate_on_submit():
        if form.image.data and form.image.data.filename:
            delete_image(s.image)
            s.image = save_image(form.image.data, 'solutions')
        s.title = form.title.data
        s.description = form.description.data
        s.icon_class = form.icon_class.data
        s.benefit_1 = form.benefit_1.data
        s.benefit_2 = form.benefit_2.data
        s.benefit_3 = form.benefit_3.data
        s.anchor_id = form.anchor_id.data
        s.order_index = form.order_index.data or 0
        s.is_published = form.is_published.data
        db.session.commit()
        flash('Solution updated!', 'success')
        return redirect(url_for('admin_solutions'))
    return render_template('admin/edit_solution.html', form=form, solution=s)


@app.route('/admin/solutions/<int:id>/delete', methods=['POST'])
@login_required
def delete_solution(id):
    s = db.get_or_404(Solution, id)
    delete_image(s.image)
    db.session.delete(s)
    db.session.commit()
    flash('Solution deleted.', 'success')
    return redirect(url_for('admin_solutions'))


# ── Admin Team ─────────────────────────────────────────────────────────────────

@app.route('/admin/team')
@login_required
def admin_team():
    team = TeamMember.query.order_by(TeamMember.order_index).all()
    return render_template('admin/manage_team.html', team=team)


@app.route('/admin/team/add', methods=['GET', 'POST'])
@login_required
def add_team_member():
    form = TeamMemberForm()
    if form.validate_on_submit():
        img_path = save_image(form.photo.data, 'team') if form.photo.data and form.photo.data.filename else None
        m = TeamMember(name=form.name.data, job_title=form.job_title.data, bio=form.bio.data,
                       photo=img_path, linkedin_url=form.linkedin_url.data,
                       order_index=form.order_index.data or 0, is_published=form.is_published.data)
        db.session.add(m)
        db.session.commit()
        flash('Team member added!', 'success')
        return redirect(url_for('admin_team'))
    return render_template('admin/add_team_member.html', form=form)


@app.route('/admin/team/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_team_member(id):
    m = db.get_or_404(TeamMember, id)
    form = TeamMemberForm(obj=m)
    if form.validate_on_submit():
        if form.photo.data and form.photo.data.filename:
            delete_image(m.photo)
            m.photo = save_image(form.photo.data, 'team')
        m.name = form.name.data
        m.job_title = form.job_title.data
        m.bio = form.bio.data
        m.linkedin_url = form.linkedin_url.data
        m.order_index = form.order_index.data or 0
        m.is_published = form.is_published.data
        db.session.commit()
        flash('Team member updated!', 'success')
        return redirect(url_for('admin_team'))
    return render_template('admin/edit_team_member.html', form=form, member=m)


@app.route('/admin/team/<int:id>/delete', methods=['POST'])
@login_required
def delete_team_member(id):
    m = db.get_or_404(TeamMember, id)
    delete_image(m.photo)
    db.session.delete(m)
    db.session.commit()
    flash('Team member deleted.', 'success')
    return redirect(url_for('admin_team'))


# ── Admin Settings ─────────────────────────────────────────────────────────────

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    site = db.session.get(SiteSettings, 1)
    if not site:
        site = SiteSettings(id=1)
        db.session.add(site)
        db.session.commit()

    site_form = SiteSettingsForm(obj=site)
    profile_form = AdminProfileForm()

    if 'save_site' in request.form and site_form.validate_on_submit():
        if site_form.company_logo.data and site_form.company_logo.data.filename:
            delete_image(site.company_logo)
            site.company_logo = save_image(site_form.company_logo.data, 'logo')
        site.company_name = site_form.company_name.data
        site.tagline = site_form.tagline.data
        site.address = site_form.address.data
        site.email = site_form.email.data
        site.phone = site_form.phone.data
        site.linkedin_url = site_form.linkedin_url.data
        site.twitter_url = site_form.twitter_url.data
        site.facebook_url = site_form.facebook_url.data
        site.instagram_url = site_form.instagram_url.data
        site.github_url = site_form.github_url.data
        db.session.commit()
        flash('Site settings saved!', 'success')
        return redirect(url_for('admin_settings'))

    if 'save_profile' in request.form and profile_form.validate_on_submit():
        if not current_user.check_password(profile_form.current_password.data):
            flash('Current password is incorrect.', 'error')
        else:
            if profile_form.profile_picture.data and profile_form.profile_picture.data.filename:
                delete_image(current_user.profile_picture)
                current_user.profile_picture = save_image(profile_form.profile_picture.data, 'admin')
            if profile_form.new_password.data:
                current_user.set_password(profile_form.new_password.data)
            db.session.commit()
            flash('Profile updated!', 'success')
        return redirect(url_for('admin_settings'))

    return render_template('admin/settings.html', site_form=site_form, profile_form=profile_form, site=site)


# ── Admin Gallery ──────────────────────────────────────────────────────────────

@app.route('/admin/gallery')
@login_required
def admin_gallery():
    galleries = Gallery.query.order_by(Gallery.order_index).all()
    return render_template('admin/manage_gallery.html', galleries=galleries)


@app.route('/admin/gallery/add', methods=['GET', 'POST'])
@login_required
def add_gallery():
    form = GalleryForm()
    if form.validate_on_submit():
        img_path = save_image(form.image.data, 'gallery') if form.image.data and form.image.data.filename else None
        if not img_path:
            flash('Failed to upload image.', 'error')
            return redirect(url_for('add_gallery'))
        gallery = Gallery(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data or 'General',
            image=img_path,
            order_index=form.order_index.data or 0,
            is_published=form.is_published.data
        )
        db.session.add(gallery)
        db.session.commit()
        flash('Image uploaded successfully!', 'success')
        return redirect(url_for('admin_gallery'))
    return render_template('admin/add_gallery.html', form=form)


@app.route('/admin/gallery/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_gallery(id):
    gallery = db.get_or_404(Gallery, id)
    form = GalleryForm(obj=gallery)
    if form.validate_on_submit():
        if form.image.data and form.image.data.filename:
            delete_image(gallery.image)
            new_img = save_image(form.image.data, 'gallery')
            if new_img:
                gallery.image = new_img
            else:
                flash('Failed to upload new image.', 'error')
                return redirect(url_for('edit_gallery', id=id))
        gallery.title = form.title.data
        gallery.description = form.description.data
        gallery.category = form.category.data or 'General'
        gallery.order_index = form.order_index.data or 0
        gallery.is_published = form.is_published.data
        db.session.commit()
        flash('Image updated!', 'success')
        return redirect(url_for('admin_gallery'))
    return render_template('admin/edit_gallery.html', form=form, gallery=gallery)


@app.route('/admin/gallery/<int:id>/delete', methods=['POST'])
@login_required
def delete_gallery(id):
    gallery = db.get_or_404(Gallery, id)
    delete_image(gallery.image)
    db.session.delete(gallery)
    db.session.commit()
    flash('Image deleted successfully.', 'success')
    return redirect(url_for('admin_gallery'))


# ── Error Handlers ─────────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    )
