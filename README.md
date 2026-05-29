# Product Website

A comprehensive Flask-based product website with admin panel for managing content including events, articles, testimonials, solutions, team members, and customer enquiries.

## Features

- **Public Website**: Showcase your products, solutions, articles, events, testimonials, and case studies
- **Admin Panel**: Manage all content with an intuitive dashboard
- **User Management**: Add and manage team members
- **Content Management**: Create, edit, and delete articles, events, solutions, and testimonials
- **Enquiry System**: Collect and manage customer inquiries
- **File Upload**: Support for image uploads in multiple categories
- **Authentication**: Secure admin login system
- **Responsive Design**: Mobile-friendly interface

## Project Structure

```
product_website/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── forms.py               # WTForms for all forms
├── seed.py                # Database seeding script
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── static/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   └── uploads/          # User-uploaded files
│       ├── events/
│       ├── articles/
│       ├── testimonials/
│       ├── solutions/
│       ├── team/
│       └── logo/
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── solutions.html    # Solutions page
    ├── case_studies.html # Case studies page
    ├── testimonials.html # Testimonials page
    ├── articles.html     # Articles listing
    ├── article_detail.html # Article detail page
    ├── events.html       # Events page
    ├── contact.html      # Contact/Enquiry form
    ├── 404.html          # 404 error page
    ├── 500.html          # 500 error page
    └── admin/            # Admin templates
        ├── login.html
        ├── dashboard.html
        ├── manage_*.html
        ├── add_*.html
        ├── edit_*.html
        └── settings.html
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd product_website
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

5. **Seed the database (optional)**
   ```bash
   python seed.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:5000`

## Default Admin Credentials (After Seeding)

- **Username**: admin
- **Password**: admin123

**Important**: Change these credentials immediately in production!

## Usage

### Public Website
- Visit `http://localhost:5000/` to access the public website
- Browse solutions, articles, events, testimonials, and case studies
- Submit contact enquiries through the contact form

### Admin Panel
- Navigate to `http://localhost:5000/admin/login`
- Login with admin credentials
- Use the dashboard to manage all content
- Create, edit, delete events, articles, testimonials, solutions, and team members
- View and manage customer enquiries
- Change admin password in settings

## Database Models

### Event
- Title, Description, Date, Location, Image

### Article
- Title, Slug, Content, Excerpt, Featured Image, Author, Published Status

### Testimonial
- Client Name, Company, Position, Content, Image, Rating, Published Status

### Solution
- Title, Description, Features, Image, Published Status

### TeamMember
- Name, Position, Bio, Email, Image, Social Links

### Enquiry
- Name, Email, Subject, Message, Status, Created Date

### CaseStudy
- Title, Slug, Client, Challenge, Solution, Results, Image, Published Status

### Admin
- Username, Email, Password Hash, Active Status

## Configuration

Edit environment variables in `app.py`:
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string (default: SQLite)
- `UPLOAD_FOLDER`: Path for uploads
- `MAX_CONTENT_LENGTH`: Maximum upload file size

## File Upload

Supported file types: PNG, JPG, JPEG, GIF
Maximum file size: 16MB

## API Routes

### Public Routes
- `GET /` - Home page
- `GET /solutions` - Solutions listing
- `GET /case-studies` - Case studies listing
- `GET /testimonials` - Testimonials listing
- `GET /articles` - Articles listing
- `GET /articles/<slug>` - Article detail
- `GET /events` - Events listing
- `GET|POST /contact` - Contact form

### Admin Routes
- `GET|POST /admin/login` - Admin login
- `GET /admin/logout` - Admin logout
- `GET /admin/dashboard` - Dashboard
- CRUD operations for events, articles, testimonials, solutions, team members, enquiries

## Security Considerations

1. Change default admin credentials immediately
2. Use strong SECRET_KEY in production
3. Implement HTTPS in production
4. Use environment variables for sensitive data
5. Regularly update dependencies
6. Implement rate limiting for forms
7. Add CORS headers if needed

## Troubleshooting

### Database not found
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

### Port already in use
```bash
# Change the port in app.py
app.run(debug=True, port=5001)
```

### Static files not loading
Ensure `static/` folder exists and `app.py` is in the project root

## Dependencies

- Flask 3.0.0 - Web framework
- Flask-SQLAlchemy 3.1.1 - ORM
- Flask-WTF 1.2.1 - Form handling
- WTForms 3.1.1 - Form library
- Werkzeug 3.0.1 - WSGI utilities

## License

This project is provided as-is for educational and business purposes.

## Support

For issues or questions, please refer to the documentation or contact support.
