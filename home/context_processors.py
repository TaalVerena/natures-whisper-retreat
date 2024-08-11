from datetime import datetime


def current_year(request):
    """
    Add the current year to the context.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary with the current year.
    """
    # Calculate the current year
    return {"current_year": datetime.now().year}
