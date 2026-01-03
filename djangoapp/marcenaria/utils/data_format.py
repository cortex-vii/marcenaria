def format_decimal(value, casas=2):
    try:
        return round(float(value), casas)
    except (TypeError, ValueError):
        return 0.0