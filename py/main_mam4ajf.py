"""Create the AJF MAM variant (similar to the Sefaria variant) from the XML MAM."""

from pycmn import bib_locales as tbn
from pysefaria import mam4sef_or_ajf
from pysefaria import mam4ajf_handlers


def almost_main():
    """Create the AJF MAM from the XML MAM."""
    variant = {
        "variant-vtrad": tbn.VT_BHS,
        "variant-handlers": mam4ajf_handlers.HANDLERS,
        "variant-path-qual": "vpq-ajf",
        "variant-exclude-header-from-csv": True,
        "variant-include-abcants": True,
    }
    mam4sef_or_ajf.main_helper(variant)


def main():
    """Create the AJF MAM from the XML MAM."""
    almost_main()


if __name__ == "__main__":
    main()
