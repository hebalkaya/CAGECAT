"""
Runs the CAGECAT web service
"""

# own project imports
from cagecat import app

### Configure Flask App Debugging
# Only for development mode. To be removed in deployment.

app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

### main code
if __name__ == "__main__":
    app.run()
