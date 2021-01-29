class StatusException(Exception):
    def __init__(self, msg):
        super(StatusException, self).__init__(msg)


def parse_error(error_msg):
    # print(error_msg)
    # print(type(error_msg))
    return str(error_msg).split()[0]

def fetch_base_error_message(error, request):
    return f"CODE:{parse_error(error)}, URL:{request.url}"


def format_status_message(status): #TODO: can probably be removed
    msg = ["Job status:"]
    if status == "queued":
        pass
    elif status == "running":
        pass
    elif status == "finished":
        pass
    else:
        raise StatusException()

    return msg