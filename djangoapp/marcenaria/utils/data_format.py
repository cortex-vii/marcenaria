def format_decimal(value, casas=2):
    try:
        valor = float(value)
        return f"{valor:.{casas}f}"
    except (TypeError, ValueError):
        return "0.00"