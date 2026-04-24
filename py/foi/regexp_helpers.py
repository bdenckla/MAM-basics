def nsqb(inner):
    """Negated square brackets."""
    return sqb(f"^{inner}")


def sqb(inner):
    """Square brackets."""
    return f"[{inner}]"


def sqbq(inner):
    """Square brackets followed by question mark."""
    return sqb(inner) + "?"


def par(inner):
    """Parentheses (capture group)."""
    return f"({inner})"


def ncpar(inner, quantifier=""):
    """Non-capturing parentheses plus maybe '+', '?', etc."""
    return par(f"?:{inner}") + quantifier


def ngs(expr):
    """Non-greedy star."""
    return f"{expr}*?"


LETT = sqb("א-ת")
NLETT = nsqb("א-ת")
ZM_NL = NLETT + "*"  # zero or more non-letters
GUTT = sqb("אהחע")  # gutturals
NGUTT = nsqb("אהחע")
XATEF = sqb(r"\u05b1\u05b2\u05b3")
