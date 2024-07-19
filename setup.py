import subprocess
import sys

def install_dependencies():
    try:
        # Install Flask and other dependencies from requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_application():
    try:
        # Install dependencies first
        print("Installing dependencies...")
        install_dependencies()

        # Run table creation script
        print("Creating database tables...")
        subprocess.check_call([sys.executable, "file_uploading/table_creation.py"])

        print("Setup complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error setting up application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_application()
