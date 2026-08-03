"""Exports MAIL_AND_CONFIRMED."""


def _multi_confirmed(email, conf1, conf2):
    return (email, conf1), (email, conf2)


MAIL_AND_CONFIRMED = {
    #
    "Fake Author": (None, None),
    #
    "Seth (Avi) Kadish": _multi_confirmed("skadish1@gmail.com", "true", "2020.07.16"),
    "Moshe Greenberg": _multi_confirmed("moshegreenberg312@gmail.com", "true", "yes"),
    "Asael Reiter": _multi_confirmed("asaelr@gmail.com", "true", "false"),
    #
    "Anonymous": _multi_confirmed(None, None, "false"),
    #
    "cvk": _multi_confirmed(None, None, "true"),
    "CVK": ((None, None), ("mail@cvkimball.com", "true")),
    "Dotan BHLA: CVK": (None, "false"),
    #
    "Daniel Holman": ("daniel.holman@mail.com", "true"),
    "Ben Denckla": ("bdenckla@alum.mit.edu", "true"),
    "Allan Johnson": ("allan_johnson@wycliffe.org", "true"),
    "Gary Luhovey": ("gluho@timbarabooks.org", "true"),
    "Yanir Marmor": ("123yanirmr@gmail.com123", "true"),
    "Graham Thomason": ("Graham.Thomason@FarAboveAll.net", "2020.01.26"),
    "Shmuel Weissman": ("shmuel@sefaria.org", "2020.01.27"),
    "Stephen Salisbury": ("Steve@grovescenter.org", "true"),
    "Yishai Glasner": ("yishai@sefaria.org", "true"),
    "Charles Loder": ("charles.w.loder@gmail.com", "true"),
    "David Reimer": ("djr24@st-andrews.ac.uk", "true"),
    #
    "Alexander Adler": ("alexander.adler0@googlemail.com", "false"),
    "Zev Farkas": ("zev.farkas@gmail.com", "false"),
    #
    "Shalom Hakkohen": (None, "false"),
    "Jonah Rank": (None, "false"),
    "Moshe Escott": (None, "false"),
    "Shmuel Schreiber": (None, "false"),
    "Todd Shandelman": (None, "false"),
}
