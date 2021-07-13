"""Runs the multicblaster web service

Author: Matthias van den Belt
"""

# own project imports
from multicblaster import app
import os

### main code
if __name__ == "__main__":
    if not os.path.exists(app.config["DATABASE_FOLDER"]):
        os.makedirs(app.config["DATABASE_FOLDER"], exist_ok=True)

    app.run()
