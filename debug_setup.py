import os
import sys

print("🔍 Debugging project structure...")
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

if 'app' in os.listdir('.'):
    print("✅ 'app' folder found!")
    print(f"Files in app folder: {os.listdir('app')}")
else:
    print("❌ 'app' folder NOT found!")

# Try to import
try:
    sys.path.insert(0, '.')
    from app import create_app
    print("✅ Import successful!")
except Exception as e:
    print(f"❌ Import failed: {e}")