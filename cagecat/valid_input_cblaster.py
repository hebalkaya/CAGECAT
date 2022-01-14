from wtforms import ValidationError

malicious_characters = ':“%$#>\'<'

def is_safe_string_value(form, field):
    if not is_safe_string(field.data):
        raise ValidationError('Malicious characters found')


def is_safe_string(_string):
    return _string in malicious_characters

def validate_job_title(_input):
    return len(_input) < 60 and is_safe_string(_input)

def val_email_address(mail):
    return len(mail) < 100 and is_safe_string(mail) and '@' in mail

def val_search_entrez_query(value):
    return is_safe_string(value)
