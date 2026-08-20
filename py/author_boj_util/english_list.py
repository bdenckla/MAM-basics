"""Format a list of items as an English phrase with 'and'."""


def english_list(elements: list[str]) -> str:
    """Format elements as 'a', 'a and b', or 'a, b, and c'."""
    assert len(elements) >= 1
    if len(elements) == 1:
        return elements[0]
    if len(elements) == 2:
        return f"{elements[0]} and {elements[1]}"
    return ", ".join(elements[:-1]) + f", and {elements[-1]}"
