# Navigating MAM-parsed plus (MPP) JSON

Full documentation lives at `../MAM-parsed/doc/reading-mam-parsed-plus.md`.

## File naming

Files are at `../MAM-parsed/plus/<book>.json` with abbreviated names:
- `A5-Deuter.json` (not `A5-Deuteronomy.json`)
- `BC-Kings.json` (not `BC-Kings_II.json`)
- `BA-Samuel.json` (not `BA-Samuel_I.json`)

Use `ls ../MAM-parsed/plus/` to see the exact names.

## Structure

```
{ "header": { "he_to_int": {"א": 1, "ב": 2, ...}, ... },
  "book39s": [
    { "chapters": {
        "א": {                // chapter 1
          "א": [D, CP, EP],   // verse 1
          "ב": [D, CP, EP],   // verse 2
          ...
        },
        ...
      }
    }
  ]
}
```

## Verse lookup by integer chapter:verse

Use the header's `he_to_int` to build a reverse mapping:

```python
int_to_he = {v: k for k, v in header["he_to_int"].items()}
verse = chapters[int_to_he[chapter_int]][int_to_he[verse_int]]
ep_column = verse[2]  # the text column
```

## Multi-book files (Samuel, Kings, Chronicles, Ezra-Nehemiah, The 12)

These have multiple entries in `book39s`. E.g. `BC-Kings.json` has
`book39s[0]` for Kings I and `book39s[1]` for Kings II.

## Template format

```json
{
  "tmpl_name": "נוסח",
  "tmpl_params": {"1": <arg1>, "2": <arg2>, "סדר": <named_arg>}
}
```

- All templates use `tmpl_params` exclusively — there is no `tmpl_args`
- Positional args use integer string keys `"1"`, `"2"`, …
- Named args (e.g. `סדר`) use their name as key
- `tmpl_params` is absent only when the template has no params at all
