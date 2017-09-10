"""Helper utilities."""
import os


def get_absolute_path(file_name, package_level=True):
    """Get file path given file name."""
    if package_level:
        # Inside `gmail_api_wrapper`
        dirname = os.path.dirname(__file__)
    else:
        # Outside `gmail_api_wrapper`
        dirname = os.path.join(os.path.dirname(__file__), os.pardir)

    file_path = os.path.abspath(os.path.join(dirname, file_name))
    return file_path


def read_file(file_name, package_level=True):
    """Get file content given file path.

    :param: file_name:string - name of file
    """
    file_path = get_absolute_path(file_name, package_level=package_level)

    with open(file_path) as file_descriptor:
        content = file_descriptor.read()
    return content


def parse_string_to_date(date_to_format):
    """Format date.

    :param: date_to_string:string - Date in String Format
    """
    try:
        from dateutil import parser
        return parser.parse(date_to_format)
    except (ImportError,):
        pass
