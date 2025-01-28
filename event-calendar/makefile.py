import subprocess
import os
import sys
import webbrowser
import time

# Define the virtual environment directory and requirements file
VENV_DIR = 'venv'
REQUIREMENTS_FILE = 'requirements.txt'

# Superuser credentials
SUPERUSER_USERNAME = 'admin'
SUPERUSER_EMAIL = 'admin@example.com'
SUPERUSER_PASSWORD = '123'

def create_venv():
    """Create a virtual environment."""
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', VENV_DIR])
    else:
        print("Virtual environment already exists.")

def install_requirements():
    """Install requirements from requirements.txt."""
    print("Installing dependencies from requirements.txt...")
    subprocess.run([os.path.join(VENV_DIR, 'Scripts', 'pip'), 'install', '-r', REQUIREMENTS_FILE])

def create_superuser():
    """Create a Django superuser."""
    print("Creating superuser...")
    
    # Use subprocess to run the createsuperuser command
    command = [
        os.path.join(VENV_DIR, 'Scripts', 'python'),
        'manage.py',
        'createsuperuser',
        '--noinput',  # Avoid interactive input
        '--username', SUPERUSER_USERNAME,
        '--email', SUPERUSER_EMAIL
    ]
    
    # Run the command to create the superuser
    subprocess.run(command)
    
    # Set the superuser's password
    subprocess.run([
        os.path.join(VENV_DIR, 'Scripts', 'python'),
        'manage.py',
        'shell',
        '-c', f"from django.contrib.auth.models import User; user = User.objects.get(username='{SUPERUSER_USERNAME}'); user.set_password('{SUPERUSER_PASSWORD}'); user.save()"
    ])

def run_django_server():
    """Run the Django development server."""
    print("Running Django server...")
    server_process = subprocess.Popen([os.path.join(VENV_DIR, 'Scripts', 'python'), 'manage.py', 'runserver'])

    # Wait for the server to start (give it some time)
    time.sleep(5)
    
    # Open the URL in the browser after the server starts
    webbrowser.open("http://127.0.0.1:8000/admin/")

    # Wait for the server to start (give it some time)
    time.sleep(10)

    # Open the URL in the browser after the server starts
    webbrowser.open("http://127.0.0.1:8000")

    # Keep the server running
    server_process.wait()

def main():
    create_venv()
    install_requirements()
    create_superuser()
    run_django_server()
    print("Server is running. Visit http://127.0.0.1:8000/admin/ login and open http://127.0.0.1:8000 in your browser.")

if __name__ == "__main__":
    main()
