from wtforms import ValidationError

malicious_characters = ':“%$#>\'<'

def is_safe_string_value(form, field):
    unsafe_string, is_safe = is_safe_string(field.data)
    if not is_safe:
        raise ValidationError(f'Malicious character found: {unsafe_string}')

def is_safe_string(_string):
    for char in _string:
        if char in malicious_characters:
            return char, False
    return None, True
    # return _string in malicious_characters

def validate_job_title(_input):
    return len(_input) < 60 and is_safe_string(_input)

def val_email_address(mail):
    return len(mail) < 100 and is_safe_string(mail) and '@' in mail

def val_search_entrez_query(value):
    return is_safe_string(value)
