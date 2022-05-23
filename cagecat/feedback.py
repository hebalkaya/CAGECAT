from flask import request, url_for

from cagecat import app
from cagecat.general_utils import show_template, send_email
from config_files.sensitive import sender_email

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback() -> str:
    """Page which handles submitted feedback

    Input:
        - No input

    Output:
        - HTML represented in string format
    """
    for email in (sender_email, request.form['email']):
        send_email('CAGECAT feedback report',
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

    return show_template('redirect.html', url=url_for('feedback.feedback_submitted'))


@app.route('/feedback-submit')
def feedback_submitted() -> str:
    """Shows a page to the user indicating their feedback has been submitted

    Output:
        - HTML represented in string format
    """
    return show_template('feedback_submitted.html', help_enabled=False)
