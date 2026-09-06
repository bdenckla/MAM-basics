# Navigating MAM-parsed-plus JSON

Full documentation lives at [Reading MAM-parsed plus](https://bdenckla.github.io/MAM-basics/MAM-parsed/plus/html/mpplus.html).

## File naming

Files are at `MAM-parsed/plus/<book>.json` with abbreviated names:
- `A5-Deuter.json` (not `A5-Deuteronomy.json`)
- `BC-Kings.json` (not `BC-Kings_II.json`)
- `BA-Samuel.json` (not `BA-Samuel_I.json`)

Use `ls MAM-parsed/plus/` to see the exact names.

## Structure

```
{ "header": { ... },
  "book39s": [
    { "chapters": {
        "1": {              // chapter 1
          "1": [C, D, E],   // verse 1
          "2": [C, D, E],   // verse 2
          ...
        },
        ...
      }
    }
  ]
}
```

## Verse lookup by integer chapter:verse

Chapter and verse keys are decimal strings, so integer lookup is direct:

```python
verse = chapters[str(chapter_int)][str(verse_int)]
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
