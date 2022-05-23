"""File to store notifications that should be rendered.

Notifications should be manually added here, uwsgi should be reloaded
by running

uwsgi --reload /tmp/uwsgi-master.pid

After a notification is no longer required, comment it out. Do not include dots
end the end of your sentence.

Author: Matthias van den Belt
"""

# format: [(notification_id, notification_text), ...].

# Notification_id should be incremented manually. Incrementing is crucial as this
# will differentiate between different notifications for correct cookie use.

notifications = [
    # ('notification_0', 'This is an example notification')

]
