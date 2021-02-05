# HTML generators
SESSION_FILE_UPLOAD = '<input type="file" required="required" ' \
                      'name="sessionFile"/>'

def generate_output_filename_form(default: str):
    return f'<input type="text" value="{default}" required="required" ' \
           f'name="outputFileName"/>'
