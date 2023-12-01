def remove_chars(input_string, chars_to_remove):
    # Create a translation table
    translation_table = str.maketrans("", "", chars_to_remove)

    return input_string.translate(translation_table)
