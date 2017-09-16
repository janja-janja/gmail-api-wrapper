"""Helper utilities."""
import os


def get_absolute_path(file_name, package_level=True):
    """Get file path given file name.

    :param: [package_level] - Wheather the file is in/out side the
    `gmail_api_wrapper` package
    """
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

    :param: [package_level] - Wheather the file is in/out side the
    `gmail_api_wrapper` package
    """
    file_path = get_absolute_path(file_name, package_level=package_level)

    with open(file_path) as file_descriptor:
        content = file_descriptor.read()
    return content


def parse_string_to_date(date_to_format):
    """Format date.

    :param: date_to_string - Date Object in String Format
    """
    try:
        from dateutil import parser
        return parser.parse(date_to_format)
    except (ImportError,):
        pass
