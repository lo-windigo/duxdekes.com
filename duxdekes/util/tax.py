from decimal import Decimal as D


NY_SALES_TAX = D(.07)


def calculate_sales_tax(amount):
    
    if amount.__class__ is not D:
        amount = D(amount)

    return amount * NY_SALES_TAX

