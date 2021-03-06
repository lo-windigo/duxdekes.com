from decimal import Decimal as D
import statestyle


def calculate_tax(price, rate):
    tax = price * rate
    return tax.quantize(D('0.01'))


def apply_to(submission):
    # Apply 7% tax to New York residents
    STATE_TAX_RATES = {
        'NY': D('0.07')
    }
    shipping_address = submission['shipping_address']

    try:
        state_object = statestyle.get(shipping_address.state)
        state = state_object.postal
        rate = STATE_TAX_RATES[state.upper()]
    except:
        rate = D('0.00')

    for line in submission['basket'].all_lines():
        line_tax = calculate_tax(
            line.line_price_excl_tax_incl_discounts, rate)
        unit_tax = (line_tax / line.quantity).quantize(D('0.01'))
        line.purchase_info.price.tax = unit_tax

    # Note, we change the submission in place - we don't need to
    # return anything from this function
    #shipping_method = submission['shipping_method']
    #shipping_method.tax = calculate_tax(
    #    shipping_method.charge_incl_tax, rate)

