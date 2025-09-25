import os
import sys

print("📁 CURRENT DIRECTORY STRUCTURE:")
print(f"Working directory: {os.getcwd()}")
print("\n📂 Files in current directory:")
for item in os.listdir('.'):
    print(f"  - {item}")

if os.path.exists('app'):
    print("\n📂 Files in 'app' directory:")
    for item in os.listdir('app'):
        print(f"  - {item}")

    if os.path.exists('app/__init__.py'):
        print("\n📄 Contents of app/__init__.py:")
        with open('app/__init__.py', 'r') as f:
            content = f.read()
            print(content)
    else:
        print("❌ app/__init__.py does not exist!")
else:
    print("❌ 'app' directory does not exist!")