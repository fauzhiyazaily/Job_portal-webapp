import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 SIMPLE IMPORT TEST")

# Test 1: Check if we can import the app package
try:
    import app

    print("✅ 'app' package imported successfully")
except ImportError as e:
    print(f"❌ Cannot import app package: {e}")
    sys.exit(1)

# Test 2: Check what's in the app package
print("\n📦 Contents of app package:")
for attr in dir(app):
    if not attr.startswith('_'):
        print(f"  - {attr}")

# Test 3: Try to import create_app directly
print("\n🔍 Trying to import create_app...")
try:
    from app import create_app

    print("✅ create_app imported successfully!")

    # Test 4: Try to create app instance
    app_instance = create_app()
    print("✅ App instance created successfully!")
    print(f"   App name: {app_instance.name}")
    print(f"   App secret key: {app_instance.config['SECRET_KEY']}")

except ImportError as e:
    print(f"❌ Cannot import create_app: {e}")
except Exception as e:
    print(f"❌ Error creating app: {e}")