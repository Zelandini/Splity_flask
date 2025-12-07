from Splity import create_app
import os

app = create_app()

print("App created successfully!")
print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Check if instance folder exists
if os.path.exists('instance'):
    print("✓ Instance folder exists")
    files = os.listdir('instance')
    print(f"Files in instance/: {files}")
else:
    print("✗ Instance folder does NOT exist")

# Check if db file exists
if os.path.exists('instance/splity.db'):
    print("✓ Database file exists!")
    size = os.path.getsize('instance/splity.db')
    print(f"Database size: {size} bytes")
else:
    print("✗ Database file does NOT exist")