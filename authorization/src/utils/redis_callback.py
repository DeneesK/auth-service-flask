def decode_resp(arg):
    try:
        return arg.decode()
    except AttributeError:
        return arg