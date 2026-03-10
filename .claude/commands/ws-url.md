Given a book name and chapter number, construct the Hebrew Wikisource MAM (te'amim) URL.

The URL pattern is:
```
https://he.wikisource.org/wiki/{name_he}_{he_chapter}/טעמים
```

Where:
- `{name_he}` is the Hebrew book name (spaces replaced with underscores in the URL)
- `{he_chapter}` is the chapter number in Hebrew numerals (gematria)

Hebrew book names (from mgketer book_metadata.py):
- Genesis = בראשית
- Exodus = שמות
- Leviticus = ויקרא
- Numbers = במדבר
- Deuteronomy = דברים
- Joshua = יהושע
- Judges = שופטים
- 1Samuel = שמואל א
- 2Samuel = שמואל ב
- 1Kings = מלכים א
- 2Kings = מלכים ב
- Isaiah = ישעיהו
- Jeremiah = ירמיהו
- Ezekiel = יחזקאל
- Hosea = הושע
- Joel = יואל
- Amos = עמוס
- Obadiah = עובדיה
- Jonah = יונה
- Micah = מיכה
- Nahum = נחום
- Habakkuk = חבקוק
- Zephaniah = צפניה
- Haggai = חגי
- Zechariah = זכריה
- Malachi = מלאכי
- Psalms = תהלים
- Proverbs = משלי
- Job = איוב
- Song of Songs = שיר השירים
- Ruth = רות
- Lamentations = איכה
- Ecclesiastes = קהלת
- Esther = אסתר
- Daniel = דניאל
- Ezra = עזרא
- Nehemiah = נחמיה
- 1Chronicles = דברי הימים א
- 2Chronicles = דברי הימים ב

Hebrew numeral conversion (gematria, no geresh/gershayim):
- 1=א, 2=ב, 3=ג, 4=ד, 5=ה, 6=ו, 7=ז, 8=ח, 9=ט
- 10=י, 20=כ, 30=ל, 40=מ, 50=נ, 60=ס, 70=ע, 80=פ, 90=צ, 100=ק
- Combine tens+ones (e.g. 19=יט, 37=לז)
- Sacred-name remaps: 15=טו (not יה), 16=טז (not יו), 115=קטו, 116=קטז

The URL should be percent-encoded for the Hebrew characters. Provide the result as a clickable markdown link where the link text is the readable (non-encoded) URL and the href is the percent-encoded URL.

Example: 2Kings chapter 19
- name_he = מלכים ב
- chapter 19 in Hebrew = יט
- [https://he.wikisource.org/wiki/מלכים_ב_יט/טעמים](https://he.wikisource.org/wiki/%D7%9E%D7%9C%D7%9B%D7%99%D7%9D_%D7%91_%D7%99%D7%98/%D7%98%D7%A2%D7%9E%D7%99%D7%9D)

User input: $ARGUMENTS
