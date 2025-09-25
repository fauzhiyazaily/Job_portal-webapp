import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category


def initialize_database():
    # Create app instance
    app = create_app()

    with app.app_context():
        # Create all tables
        db.create_all()

        # Add sample categories
        categories = ['Technology', 'Healthcare', 'Finance', 'Education', 'Marketing', 'Sales']
        for cat_name in categories:
            if not Category.query.filter_by(name=cat_name).first():
                category = Category(name=cat_name)
                db.session.add(category)

        db.session.commit()
        print("✅ Database initialized successfully!")
        print("✅ Sample categories added!")


if __name__ == '__main__':
    initialize_database()