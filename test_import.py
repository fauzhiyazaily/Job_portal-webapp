import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Testing imports...")

try:
    from app import create_app

    print("✅ create_app import successful!")

    app = create_app()
    print("✅ App creation successful!")
    print(f"✅ App name: {app.name}")

    # Test database
    with app.app_context():
        from app import db

        db.create_all()
        print("✅ Database tables created!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()