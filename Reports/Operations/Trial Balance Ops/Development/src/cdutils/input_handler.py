def accept_user_input() -> int|str:
    """
    Accept user input via command line. User input is sanitizated during this function as well, although it may be sanitized earlier too.

    Returns:
        filter_key (int): Key to filter on
        email (int): Valid '@bcsbmail.com' email
    """
    # Porfolio key/Household key
    filter_key = int(input("Please enter Household Key to filter on: "))

    # Email
    email = str(input("Please enter email to receive status page: "))

    # # Household Title
    # household_title = str(input("Please enter proposed household title"))

    return filter_key, email