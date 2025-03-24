def get_value_for_discriminator(values, key: str):
    if isinstance(values, dict):
        return values.get(key, None)
    else:
        return getattr(values, key, None)
