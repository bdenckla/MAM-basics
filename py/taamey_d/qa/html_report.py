HTML_HEADER = """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>{} Report</title>
        <style type="text/css">
            @font-face {{ font-family: "TestFont"; src: url({}); }}
            .tf {{ font-family: "TestFont"; font-size: 3rem; }}
            html {{ font-family: sans-serif; background-color: lightgray; }}
            h2 {{ background: #77f; color: #fafafa; padding: 12px; }}
            pre {{ font-size: 0.8rem; }}
            li {{ font-size: 1.0rem; border-top: 1px solid #ddd; padding: 12px; margin-top: 12px; }}
            svg {{ height: 100px; margin:10px; transform: matrix(1, 0, 0, -1, 0, 0); }}
        </style>
    </head>
    <body>
"""
HTML_FOOTER = """
    </body>
<html>
"""


def span_tf(x):
    return f'<span class="tf">{x}</span>'


def report_to_html(
    html_file,
    vhb,
    message,
    text=None,
    buf1=None,
    buf2=None,
    type="item",
    extra_data=None,
    expected_str=None,
):
    # expected_str is the fallback for buf2: the caller passes it when it has an
    # expected serialization but could not turn it into a buffer, e.g. because the
    # serialization names a glyph the font does not have.
    if text:
        message = message + ": " + span_tf(text)

    if type == "item":
        message = "<li>%s</li>" % message
    if type == "header":
        message = "<h2>%s</h2>" % message
    html_file.write(message + "\n")
    if extra_data:
        html_file.write("<pre>%s</pre>" % extra_data)
    if buf1:
        html_file.write("<pre>Got     : %s</pre>" % vhb.serialize_buf(buf1))
    if buf2:
        html_file.write("<pre>Expected: %s</pre>" % vhb.serialize_buf(buf2))
    elif expected_str:
        html_file.write("<pre>Expected: %s</pre>" % expected_str)
    if buf1:
        html_file.write("Got:")
        html_file.write(vhb.buf_to_svg(buf1))
    if buf2:
        html_file.write("Expected:")
        html_file.write(vhb.buf_to_svg(buf2))
