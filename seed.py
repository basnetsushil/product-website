from app import app, db
from models import AdminUser, SiteSettings, Solution, Article, Event, Testimonial, TeamMember
from datetime import datetime, timedelta

def seed_database():
    with app.app_context():
        print("🌱 Seeding database... please wait.")

        # 1. Clean existing data to avoid duplicates
        db.drop_all()
        db.create_all()

        # 2. Create Admin User
        admin = AdminUser(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        # 3. Create Site Settings
        settings = SiteSettings(
            company_name="AI-Solutions",
            tagline="Architecting the Intelligence of Tomorrow in the Heart of Sunderland.",
            address="123 Tech Hub, Sunderland, SR1 1AA, United Kingdom",
            email="contact@ai-solutions.co.uk",
            phone="+44 191 555 0123",
            linkedin_url="https://linkedin.com/company/ai-solutions",
            twitter_url="https://twitter.com/aisolutions_uk",
            github_url="https://github.com/ai-solutions-uk"
        )
        db.session.add(settings)

        # 4. Seed 6 Solutions
        solutions = [
            Solution(title="Predictive Analytics", description="Forecasting market trends using deep learning models.", icon_class="📈", benefit_1="Reduce risk", benefit_2="Optimize stock", benefit_3="Increase ROI", order_index=1),
            Solution(title="NLP Engine", description="Custom Large Language Models tailored for your corporate data.", icon_class="💬", benefit_1="Automate support", benefit_2="Semantic search", benefit_3="Sentiment analysis", order_index=2),
            Solution(title="Computer Vision", description="Real-time object detection and image recognition systems.", icon_class="👁️", benefit_1="Quality control", benefit_2="Security automation", benefit_3="Visual analytics", order_index=3),
            Solution(title="RPA Integration", description="Robotic Process Automation to eliminate repetitive manual tasks.", icon_class="🤖", benefit_1="Save 40% time", benefit_2="Zero human error", benefit_3="24/7 Operation", order_index=4),
            Solution(title="AI Strategy", description="Consultancy to navigate the complex landscape of AI adoption.", icon_class="🗺️", benefit_1="Roadmap design", benefit_2="Tech stack audit", benefit_3="KPI alignment", order_index=5),
            Solution(title="Edge AI", description="Deploying intelligence directly on hardware for zero-latency.", icon_class="⚡", benefit_1="No cloud lag", benefit_2="Enhanced privacy", benefit_3="Bandwidth saving", order_index=6),
        ]
        db.session.bulk_save_objects(solutions)

        # 5. Seed 4 Articles
        articles = [
            Article(title="The Future of AI in the North East", excerpt="How Sunderland is becoming a hub for AI innovation.", body="Full article content about the North East tech boom...", category="Insights", author="Dr. Sarah Chen", published_at=datetime.utcnow()),
            Article(title="Scaling LLMs for Enterprise", excerpt="Moving from a prototype to a production-ready AI system.", body="Full article about deployment strategies...", category="Technical", author="James Wilson", published_at=datetime.utcnow() - timedelta(days=2)),
            Article(title="Ethical AI Frameworks", excerpt="Why transparency is the most important feature of any AI.", body="Discussion on bias and ethics in machine learning...", category="Ethics", author="Dr. Sarah Chen", published_at=datetime.utcnow() - timedelta(days=5)),
            Article(title="Case Study: Retail Automation", excerpt="How we saved a local retailer £50k/year using AI.", body="Detailed breakdown of the retail project...", category="Case Study", author="James Wilson", published_at=datetime.utcnow() - timedelta(days=10)),
        ]
        db.session.bulk_save_objects(articles)

        # 6. Seed 4 Events
        events = [
            Event(name="Sunderland AI Summit", description="The largest AI gathering in the North East.", event_date=datetime(2024, 12, 15), location="Sunderland Stadium", is_upcoming=True),
            Event(name="ML Workshop", description="Hands-on training with PyTorch and TensorFlow.", event_date=datetime(2024, 11, 10), location="Virtual", is_upcoming=True),
            Event(name="AI Ethics Webinar", description="Discussing the future of regulation.", event_date=datetime(2024, 8, 20), location="Virtual", is_upcoming=False),
            Event(name="Tech Expo 2024", description="Showcasing our latest 3D AI interfaces.", event_date=datetime(2024, 5, 1), location="Sunderland City Centre", is_upcoming=False),
        ]
        db.session.bulk_save_objects(events)

        # 7. Seed 6 Testimonials
        testimonials = [
            Testimonial(customer_name="Alice Thompson", job_title="CEO", company="Logistics UK", quote="AI-Solutions transformed our supply chain overnight.", rating=5),
            Testimonial(customer_name="Bob Richards", job_title="CTO", company="Sunderland Retail", quote="The most professional AI team we've ever worked with.", rating=5),
            Testimonial(customer_name="Claire Zhang", job_title="Ops Manager", company="Global Tech", quote="Their NLP engine reduced our support tickets by 60%.", rating=4),
            Testimonial(customer_name="David Smith", job_title="Founder", company="StartupX", quote="Incredible vision and technical execution.", rating=5),
            Testimonial(customer_name="Emma Watson", job_title="Director", company="HealthCore", quote="Secure and efficient AI implementation.", rating=5),
            Testimonial(customer_name="Frank Miller", job_title="Lead Eng", company="AutoWorks", quote="Edge AI has completely changed our assembly line.", rating=4),
        ]
        db.session.bulk_save_objects(testimonials)

        # 8. Seed 3 Team Members
        team = [
            TeamMember(name="Dr. Sarah Chen", job_title="Chief AI Scientist", bio="Former researcher at MIT, specializing in Neural Networks.", order_index=1),
            TeamMember(name="James Wilson", job_title="Head of Engineering", bio="Full-stack architect with 15 years of experience in scalable systems.", order_index=2),
            TeamMember(name="Marcus Thorne", job_title="Product Designer", bio="Expert in immersive 3D UI and human-centered AI design.", order_index=3),
        ]
        db.session.bulk_save_objects(team)

        db.session.commit()
        print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_database()