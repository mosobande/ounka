yoruba_numbers = {
    1: "ení", 2: "èjì", 3: "ẹ̀ta", 4: "ẹ̀rin", 5: "àrún",
    6: "ẹ̀fà", 7: "èje", 8: "ẹ̀jọ", 9: "ẹ̀sán", 10: "ẹ̀wá",
    11: "óókànlá", 12: "ééjìlá", 13: "ẹ́ẹ́tàlá", 14: "ẹ́ẹ́rìnlá",
    15: "áárùdínlógún", 16: "ẹ́ẹ́rìdínlógún", 17: "ẹ́ẹ́tàdínlógún",
    18: "ééjìdínlógún", 19: "óókàndínlógún",
    20: "ogún", 30: "ọgbọ̀n", 40: "ogójì", 50: "àádọ́ta", 60: "ọgọ́ta",
    70: "àádọ́rin", 80: "ọgọ́rin", 90: "àádọ́rùún", 100: "ọgọ́rùn-ún kan",
    200: "ọgọ́rùn-ún méjì", 300: "ọgọ́rùn-ún mẹ́ta", 400: "ọgọ́rùn-ún mẹ́rin",
    500: "ọgọ́rùn-ún márùún", 600: "ọgọ́rùn-ún mẹ́fà", 700: "ọgọ́rùn-ún méje",
    800: "ọgọ́rùn-ún mẹ́jọ", 900: "ọgọ́rùn-ún mẹ́sàán"
}

yoruba_large_numbers = {
    1000: "ẹgbẹ̀rún", 1000000: "ẹgbẹ̀lẹ́gbẹ̀", 1000000000: "ẹgbẹ̀lẹ́gbèjì",
    1000000000000: "ẹgbẹ̀lẹ́gbẹ̀ta", 1000000000000000: "ẹgbẹ̀lẹ́gbẹ̀rin",
    1000000000000000000: "ẹgbẹ̀lẹ́gbàrún", 1000000000000000000000: "ẹgbẹ̀lẹ́gbẹ̀fà",
    1000000000000000000000000: "ẹgbẹ̀lẹ́gbèje", 1000000000000000000000000000: "ẹgbẹ̀lẹ́gbẹ̀jọ",
    1000000000000000000000000000000: "ẹgbẹ̀lẹ́gbẹ̀sán", 1000000000000000000000000000000000: "ẹgbẹ̀lẹ́gbẹ̀wá"
}


# Split the number into large number components (millions, billions, etc.)
def split_number(n):
    components = []
    for value in sorted(yoruba_large_numbers.keys(), reverse=True):
        if n >= value:
            quotient = n // value
            remainder = n % value
            components.append((quotient, value))
            n = remainder
    if n > 0:
        components.append((n, 1))
    return components


# Convert small numbers (1-999)
def convert_small_number(n, large=False):
    if n <= 19:
        # Handle numbers 1-19 in large contexts
        if n == 1 and large:
            return "kan"
        if n == 2 and large:
            return "méjì"
        if n == 3 and large:
            return "mẹ́ta"
        if n == 4 and large:
            return "mẹ́rin"
        if n == 5 and large:
            return "márùún"
        if n == 6 and large:
            return "mẹ́fà"
        if n == 7 and large:
            return "méje"
        if n == 8 and large:
            return "mẹ́jọ"
        if n == 9 and large:
            return "mẹ́sàán"
        if n == 10 and large:
            return "mẹ́wàá"
        if n == 11 and large:
            return "mókànlá"
        if n == 12 and large:
            return "méjìlá"
        if n == 13 and large:
            return "mẹ́tàlá"
        if n == 14 and large:
            return "mẹ́rìnlá"
        if n == 15 and large:
            return "méẹ̀dógún"
        if n == 16 and large:
            return "mẹ́rìndínlógún"
        if n == 17 and large:
            return "mẹ́tàdínlógún"
        if n == 18 and large:
            return "méjìdínlógún"
        if n == 19 and large:
            return "mókàndínlógún"
        return yoruba_numbers.get(n, str(n))  # Fallback to string representation for very large numbers
    elif n < 100:
        tens = (n // 10) * 10
        remainder = n % 10
        return yoruba_numbers.get(tens, str(tens)) + (
            " " + yoruba_numbers.get(remainder, str(remainder)) if remainder else "")
    else:
        hundreds = (n // 100) * 100
        remainder = n % 100
        return yoruba_numbers.get(hundreds, str(hundreds)) + (
            " " + convert_small_number(remainder) if remainder else "")


def number_to_yoruba(n):
    if n == 0:
        return "òdo"  # Return 'òdo' for zero in the new Yoruba system
    components = split_number(n)
    result = []

    for quotient, value in components:
        if quotient > 0:
            if value == 1:
                # Handle small numbers
                result.append(convert_small_number(quotient))
            else:
                # Handle the 1-19 exception for large numbers
                if quotient <= 19:
                    result.append(yoruba_large_numbers[value] + " " + convert_small_number(quotient, large=True))
                else:
                    result.append(convert_small_number(quotient) + " " + yoruba_large_numbers[value])

    # Join components correctly with commas between large groups, no commas between hundreds, tens, and units
    final_result = []
    for i, part in enumerate(result):
        # Add a comma only after large number groups (thousands, millions, billions, etc.)
        if i > 0 and i % 2 == 1:
            final_result.append(", " + part)
        else:
            final_result.append(part)

    # Ensure correct spacing and eliminate merged components
    output = " ".join(final_result).replace(" ,", ",").replace("  ", " ").strip()

    # Insert commas between thousands and hundreds
    output = output.replace("ẹgbẹ̀rún ọgọ́rùn-ún", "ẹgbẹ̀rún, ọgọ́rùn-ún")

    # Ensure commas between large groups like nonillion, octillion, and so on
    output = output.replace("ẹgbẹ̀lẹ́gbèje ọgọ́rùn-ún", "ẹgbẹ̀lẹ́gbèje, ọgọ́rùn-ún")
    output = output.replace("ẹgbẹ̀lẹ́gbèje mẹ́sàán", "ẹgbẹ̀lẹ́gbèje, mẹ́sàán")
    output = output.replace("ẹgbẹ̀lẹ́gbèje àádọ́rùún", "ẹgbẹ̀lẹ́gbèje, àádọ́rùún")

    output = output.replace("ẹgbẹ̀lẹ́gbàrún ọgọ́rùn-ún", "ẹgbẹ̀lẹ́gbàrún, ọgọ́rùn-ún")
    output = output.replace("ẹgbẹ̀lẹ́gbàrún mẹ́sàán", "ẹgbẹ̀lẹ́gbàrún, mẹ́sàán")
    output = output.replace("ẹgbẹ̀lẹ́gbàrún àádọ́rùún", "ẹgbẹ̀lẹ́gbàrún, àádọ́rùún")

    output = output.replace("ẹgbẹ̀lẹ́gbèje mẹ́sàán", "ẹgbẹ̀lẹ́gbèje, mẹ́sàán")
    output = output.replace("ẹgbẹ̀lẹ́gbèje àádọ́rùún", "ẹgbẹ̀lẹ́gbèje, àádọ́rùún")

    # Add commas for large number transitions
    output = output.replace("ẹgbẹ̀lẹ́gbèje ẹ̀", "ẹgbẹ̀lẹ́gbèje, ẹ̀")
    output = output.replace("ẹgbẹ̀lẹ́gbàrún ẹ̀", "ẹgbẹ̀lẹ́gbàrún, ẹ̀")
    output = output.replace("ẹgbẹ̀lẹ́gbẹ̀jọ ẹ̀", "ẹgbẹ̀lẹ́gbẹ̀jọ, ẹ̀")
    output = output.replace("ẹgbẹ̀lẹ́gbẹ̀sán ẹ̀", "ẹgbẹ̀lẹ́gbẹ̀sán, ẹ̀")

    return output


if __name__ == "__main__":
    print("Represent a number in the proposed Yoruba numbering system.")
    print("Enter a number or type 'exit' to end the application.\n")
    while True:
        try:
            user_input = input("-> ")
            if user_input.lower() == "exit":
                break
            yoruba_output = number_to_yoruba(int(user_input))
            print(
                f"{user_input} is: {yoruba_output}\n")
        except ValueError:
            print("Please enter a valid number.")
