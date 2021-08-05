"""Stores routes for Flask web application for feedback pages

Author: Matthias van den Belt
"""

from flask import Blueprint, request, url_for
from cagecat import routes_helpers as rthelp, utils as ut
from config_files.config import EMAIL

feedback = Blueprint('feedback', __name__, template_folder="templates")


@feedback.route('/')
def feedback_page() -> str:
    """Shows the feedback page to the user

    Output:
        - HTML represented in string format
    """
    return rthelp.show_template('feedback.xhtml', help_enabled=False)


@feedback.route('/submit', methods=['POST'])
def submit_feedback() -> str:
    """Page which handles submitted feedback

    Input:
        - No input

    Output:
        - HTML represented in string format
    """
    for email in (EMAIL['sender_email'], request.form['email']):
        ut.send_email('CAGECAT feedback report',
                      f'''

Thank you for your feedback report. The development team will reply as soon as possible. The team might ask you for additional information, so be sure to keep your inbox regularly.

-----------------------------------------
Submitted info:

Feedback type: {request.form['feedback_type']}
E-mail address: {request.form['email']}
Job ID: {request.form['job_id']}
Message: {request.form['message']}

-----------------------------------------''',
                      email)

    return rthelp.show_template('redirect.xhtml', url=url_for('feedback.feedback_submitted'))


@feedback.route('/submitted')
def feedback_submitted() -> str:
    """Shows a page to the user indicating their feedback has been submitted

    Output:
        - HTML represented in string format
    """
    return rthelp.show_template('feedback_submitted.xhtml', help_enabled=False)
