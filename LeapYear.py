def is_leap_year(year):
    """Checks if a given year is a leap year."""
    if (year % 4 == 0):
        if (year % 100 == 0):
            if (year % 400 == 0):
                return True  # Divisible by 400
            else:
                return False # Divisible by 100 but not 400
        else:
            return True      # Divisible by 4 but not 100
    else:
        return False         # Not divisible by 4


year_to_check = int(input("Enter a year to check: "))

if is_leap_year(year_to_check):
    print(f"{year_to_check} is a leap year!")
else:
    print(f"{year_to_check} is not a leap year.")