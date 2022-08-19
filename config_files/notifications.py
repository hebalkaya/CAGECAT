"""File to store notifications that should be rendered.

Notifications should be manually added here, uwsgi should be reloaded
by running

uwsgi --reload /tmp/uwsgi-master.pid

After a notification is no longer required, comment it out. Do not include dots
end the end of your sentence.

Author: Matthias van den Belt
"""

from config_files.config import send_mail

# format: [(notification_id, notification_text), ...].

# Notification_id should be incremented manually. Incrementing is crucial as this
# will differentiate between different notifications for correct cookie use.

notifications = [
    # ('notification_0', 'This is an example notification')

]

if not send_mail:
    to_insert = (0, 'notification_0', 'Email functionality has been disabled by your administrator. Feedback submissions or email notifications are not available')
    notifications.insert(to_insert)
