"""Ungrammatical structured research notes — 2c."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    BHS_TRANSCRIBES,
    ETNAXTA,
    MUNAX,
    TIPEXA,
)

BY_REF: dict[str, dict[str, object]] = {
    "2c 22:12": {
        "st-source": "bhs",
        "st-summary": f"BHS transcribes an {ETNAXTA} as a {TIPEXA}.",
        "wlc_focus": "שנ֖ים",
        "uxlc_change": "2024.04.01/2023.09.16-12",
        "comment": "See the image in the UXLC change to which we link above.",
    },
    "2c 7:5": {
        "st-source": "bhs",
        "wlc_focus": "ז֣בח הבק֗ר",
        "st-summary": f"BHS accents a chanted word with {MUNAX} rather than segol.",
        "uxlc_change": "2024.04.01/2023.09.16-3",
        "comment": (f"MAM has {MUNAX} segol whereas the LC has segol revia."),
    },
    "2c 8:10": {
        "st-source": "bhs",
        "wlc_focus": "שר֤י",
        "st-summary": BHS_TRANSCRIBES,
        "uxlc_change": "2024.04.01/2023.09.16-4",
    },
    "2c 24:27": {
        "st-source": "bhs",
        "wlc_focus": "י֧ר֞ב",
        "st-summary": "BHS adds a gershayim out of nowhere.",
        "img": "LC-357B-col-2-line-6-2C-24v27.png",
        "pending_uxlc_change": "2026.10.19/2026.04.10-6",
        "comment": "Perhaps the darga was accidentally repeated from the previous chanted word, which legitimately has a darga.",
    },
    "2c 25:1": {
        "st-source": "bhs",
        "wlc_focus": "ועשר֣ים",
        "st-summary": BHS_TRANSCRIBES,
        "uxlc_change": "2024.04.01/2023.09.16-13",
        "comment": (
            "See the UXLC change image. UXLC corrects WLC but places the mahapakh under the yod, an aggresively uncharitable location for it."
        ),
    },
}
