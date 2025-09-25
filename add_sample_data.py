import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Job, Category


def add_sample_data():
    print("🔄 Adding sample data...")

    app = create_app()

    with app.app_context():
        # Create a sample employer if doesn't exist
        employer = User.query.filter_by(email='employer@test.com').first()
        if not employer:
            employer = User(
                username='TechCompany',
                email='employer@test.com',
                user_type='employer'
            )
            employer.set_password('password123')
            db.session.add(employer)
            db.session.commit()
            print("✅ Created sample employer")

        # Get categories
        categories = Category.query.all()

        # Add sample jobs if none exist
        if Job.query.count() == 0:
            sample_jobs = [
                {
                    'title': 'Python Developer',
                    'description': 'We are looking for an experienced Python developer to join our team. You will be working on exciting web applications using Flask and Django.',
                    'requirements': '3+ years of Python experience, knowledge of Flask/Django, SQL databases',
                    'location': 'New York, NY',
                    'salary': '$80,000 - $100,000',
                    'job_type': 'full_time',
                    'employer_id': employer.id,
                    'category_id': categories[0].id if categories else None
                },
                {
                    'title': 'Frontend Developer',
                    'description': 'Join our frontend team to create beautiful and responsive user interfaces using modern JavaScript frameworks.',
                    'requirements': 'Experience with React, Vue.js, or Angular, CSS, HTML5',
                    'location': 'Remote',
                    'salary': '$70,000 - $90,000',
                    'job_type': 'full_time',
                    'employer_id': employer.id,
                    'category_id': categories[0].id if categories else None
                },
                {
                    'title': 'Data Analyst',
                    'description': 'Looking for a data analyst to help us make data-driven decisions and create insightful reports.',
                    'requirements': 'SQL, Python, data visualization tools, statistical analysis',
                    'location': 'Chicago, IL',
                    'salary': '$65,000 - $85,000',
                    'job_type': 'full_time',
                    'employer_id': employer.id,
                    'category_id': categories[2].id if len(categories) > 2 else None
                }
            ]

            for job_data in sample_jobs:
                job = Job(**job_data)
                db.session.add(job)

            db.session.commit()
            print("✅ Added sample jobs")

        print(f"📊 Total jobs in database: {Job.query.count()}")
        print("🎉 Sample data added successfully!")


if __name__ == '__main__':
    add_sample_data()