"""Helper utilities."""
from dateutil import parser


def read_file(file_path):
    """Get file content given file path.

    :param: file_path:string - path to file
    """
    with open(file_path) as file_descriptor:
        content = file_descriptor.read()

    return content


def parse_string_to_date(date_to_format):
    """Format date.

    :param: date_to_string:string - Date in String Format
    """
    return parser.parse(date_to_format)
