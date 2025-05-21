def normalize_file_name(string):
    r"""
    Replace slashes with `_slash_`.
    """
    return string.replace("\\", '_slash_').replace(r"/", '_slash_')
