# MAM-simple

MAM-simple is a simple but incomplete extract of Miqra According to the Masorah (MAM).
Its source is MAM's Hebrew Wikisource text, through this repository's
`MAM-parsed/plus/` product. It is available in XML and JSON, each in MAM, BHS, and
Sefaria versifications. See [MAM-parsed](../MAM-parsed/README.md) for a complete version.

## Documentation

- [Reading MAM-simple](https://bdenckla.github.io/MAM-basics/MAM-simple/reading-mam-simple.html) — file layout, consumer notice, and examples
- [XML format](https://bdenckla.github.io/MAM-basics/MAM-simple/reading-mam-simple-xml.html)
- [JSON format](https://bdenckla.github.io/MAM-basics/MAM-simple/reading-mam-simple-json.html)
- [Versification differences](https://bdenckla.github.io/MAM-basics/MAM-simple/versification-differences.html)
- [Versification and cantillation](https://bdenckla.github.io/MAM-basics/MAM-simple/versification-and-cantillation.html)

Read the [consumer notice](https://bdenckla.github.io/MAM-basics/MAM-simple/reading-mam-simple.html#consumer-notice)
before writing an application against this product.

## Sparse checkout

MAM-simple is a product tree inside [MAM-basics](https://github.com/bdenckla/MAM-basics).
To check out only this product, choose an unused destination and run:

```powershell
git clone --filter=blob:none --sparse https://github.com/bdenckla/MAM-basics.git MAM-simple-sparse
```

```powershell
git -C MAM-simple-sparse sparse-checkout set MAM-simple
```

In an existing sparse MAM-basics checkout, run:

```powershell
git -C MAM-basics sparse-checkout add MAM-simple
```

## Example program

[`main_letter_small_job_example.py`](py-examples/main_letter_small_job_example.py)
reports the `<letter-small>` elements in `Job.xml`.
The [reading guide](https://bdenckla.github.io/MAM-basics/MAM-simple/reading-mam-simple.html#the-py-examples-program-and-the-two-that-were-retired)
describes this example and the other examples that were retired.

## License and contact

MAM-simple is available under CC BY-SA 4.0. See [LICENSE.md](LICENSE.md) for the
license text and the attribution it asks for, which differs between Hebrew and every
other language.

Questions? Email maintainer@miqra.simplelogin.com.
