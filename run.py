"""Runs the multicblaster web service

Author: Matthias van den Belt
"""

# own project imports
from multicblaster import app
import os
import config

### main code
if __name__ == "__main__":
    if not os.path.exists(app.config["DATABASE_FOLDER"]):
            os.makedirs(app.config["DATABASE_FOLDER"], exist_ok=True)

    # TODO: should be from config file
    # app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///status.db'
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.run(host=app.config["HOST"], port=app.config["PORT"])

    # lets other computers within the same network access the web pages
    # by typing the following address in a web browser:
    #       "<ip_of_pc_where_this_module_is_ran_from>:5001"
