def remove_chars(input_string, chars_to_remove):
    # Creating a translation table
    translation_table = str.maketrans("", "", chars_to_remove)

    # Using translate to remove the specified characters
    result_string = input_string.translate(translation_table)

    return result_string
