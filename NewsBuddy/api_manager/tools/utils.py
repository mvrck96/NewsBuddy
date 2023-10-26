import datetime


def is_valid_date(date_str, date_format="%Y%m%dT%H%M") -> bool:
    """
    Validate if a date string is in the correct format.

    Args:
        date_str (str): The date string to validate.
        date_format (str, optional): The expected date format. Defaults to "%Y%m%dT%H%M".

    Returns:
        bool: True if the date string is in the correct format, False otherwise.
    """
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

