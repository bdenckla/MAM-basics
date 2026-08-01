family = "wikisource"
mylang = "he"
# `usernames` is not defined here: pywikibot pre-populates it in the namespace it
# execs this config file in, so a linter reading the file as an ordinary module is
# right that the name is undefined and wrong that it is a problem.
usernames["wikisource"]["he"] = "BDencklaBot"  # noqa: F821
# usernames['wikisource']['he'] = 'Bdenckla'
password_file = "password.py"
