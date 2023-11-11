*REST MOVIES*

Web Service to get movies in theaters data in real time

# Create an development environment
py -m venv ./venv

# Activate development environment
venv/Scripts/activate.bat

# Install application requirements
pip install -r requirements.txt

# Start application server with auto reload using uvicorn
uvicorn main:app --reload