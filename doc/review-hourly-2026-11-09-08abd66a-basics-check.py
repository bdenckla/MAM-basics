"""Independent sparse differential checks, not project tests or regeneration."""
import ast
from collections import Counter
from html.parser import HTMLParser
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace

ROOT = Path(__file__).parent
C = json.loads((ROOT / 'compare-full.json').read_text())
assert C['base_commit']['sha'] == '2db5d4fbe24dab0509a4fb5e92511de1535b3a6f'
assert C['commits'][-1]['sha'] == '08abd66a1452ba654e19aefc55ea0589fcd936c3'
assert C['total_commits'] == 3 and len(C['files']) == 25
MARK = re.compile(r'[\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7-\u05c9]')
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())

class Node:
    def __init__(self, tag='', attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []
    def text(self):
        return ''.join(c if isinstance(c, str) else c.text() for c in self.children)
    def canon(self):
        attrs = dict(self.attrs)
        unpointed = not MARK.search(self.text())
        if unpointed and attrs.get('lang') == 'hbo':
            del attrs['lang']
        children = ''.join(re.sub(r'\s+', '', c) if isinstance(c, str) else c.canon() for c in self.children)
        if unpointed and self.tag in ('span', 'bdi') and not attrs:
            return children
        return repr((self.tag, sorted(attrs.items()))) + '[' + children + ']'

class Parse(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.nodes = []
        self.feed(text)
        assert len(self.stack) == 1
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.nodes.append(n)
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        assert self.stack[-1].tag == tag, (tag, self.stack[-1].tag)
        self.stack.pop()
    def handle_data(self, text):
        self.stack[-1].children.append(text)

results = []

def reconstruct(old, patch):
    source = old.splitlines()
    out, cursor = [], 0
    lines = patch.splitlines()
    i = 0
    while i < len(lines):
        m = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', lines[i])
        assert m, lines[i]
        start = int(m[1]) - 1
        out.extend(source[cursor:start])
        cursor = start
        i += 1
        old_count = new_count = 0
        while i < len(lines) and not lines[i].startswith('@@ '):
            line = lines[i]
            if line.startswith('\\ No newline'):
                i += 1
                continue
            assert line[:1] in (' ', '+', '-')
            if line[0] in (' ', '-'):
                assert source[cursor] == line[1:], (cursor, source[cursor], line)
                cursor += 1
                old_count += 1
            if line[0] in (' ', '+'):
                out.append(line[1:])
                new_count += 1
            i += 1
        assert old_count == int(m[2] or 1)
        assert new_count == int(m[4] or 1)
    out.extend(source[cursor:])
    return out

for f in C['files']:
    path = f['filename']
    old, new = [(ROOT / side / path).read_text() for side in ('base', 'head')]
    patch = f['patch'].splitlines()
    assert sum(l.startswith('+') for l in patch) == f['additions'], path
    assert sum(l.startswith('-') for l in patch) == f['deletions'], path
    assert reconstruct(old, f['patch']) == new.splitlines(), path
    # The connector string contains the exact repository bytes; apply_patch adds
    # a final newline when the supplied content already ended with one.
    data = (ROOT / 'head' / path).read_bytes()
    def blob(b):
        return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    if blob(data) != f['sha']:
        assert data.endswith(b'\n') and blob(data[:-1]) == f['sha'], path
    item = {'path': path, 'head_blob_verified': True, 'complete_patch_reconstruction': True}
    if path.endswith('.py'):
        a, b = ast.parse(old), ast.parse(new)
        item['ast_equal'] = ast.dump(a) == ast.dump(b)
    else:
        a, b = Parse(old), Parse(new)
        assert re.sub(r'\s+', ' ', a.root.text()).strip() == re.sub(r'\s+', ' ', b.root.text()).strip(), path
        assert a.root.canon() == b.root.canon(), path
        before = [n for n in a.nodes if n.attrs.get('lang') == 'hbo']
        after = [n for n in b.nodes if n.attrs.get('lang') == 'hbo']
        pointed = lambda nodes: Counter(re.sub(r'\s+', ' ', n.text()).strip() for n in nodes if MARK.search(n.text()))
        assert pointed(before) == pointed(after), path
        item.update(hbo_removed=len(before)-len(after), pointed_elements_preserved=sum(pointed(after).values()), canonical_markup_equal=True)
    results.append(item)

def extract(path, names, env):
    tree = ast.parse((ROOT / 'head' / path).read_text())
    tree.body = [n for n in tree.body if (isinstance(n, ast.FunctionDef) and n.name in names) or (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in n.targets))]
    exec(compile(tree, path, 'exec'), env)
    return SimpleNamespace(**env)

author = extract('py/mb_author/author.py', {'is_unpointed_hebrew', '_text_of', '_HEBREW_MARK_RE', '_HEBREW_LETTER_RE'}, {'re': re})
# Only HTML constructors are doubled; classification/guard bodies are exact-head.
h = SimpleNamespace(span=lambda s, a: ('span', s, a), bdi=lambda s: ('bdi', s))
shared = extract('py/accgram/almost_errors_html_shared.py', {'hbo', 'unpointed', '_HEBREW_MARK_RE'}, {'re': re, 'author': author, 'H': h})
media = extract('py/accgram/rtmsr_media.py', {'_is_pointed_hebrew_segment', '_HEBREW_LETTER_RE'}, {'re': re, 'author': author})
notes = extract('py/py_wlc_a_notes/my_wlc_a_notes_full.py', {'_hebrew_span'}, {'author': author, 'wlc_utils_html': h})
for cp in range(0x590, 0x600):
    text = chr(0x5d0) + chr(cp)
    pointed = bool(MARK.search(text))
    assert media._is_pointed_hebrew_segment(text) == pointed
    assert notes._hebrew_span(text)[0] == ('span' if pointed else 'bdi')
    try:
        shared.hbo(text)
    except ValueError:
        assert not pointed
    else:
        assert pointed
    assert shared.hbo(text, lifted=True)[0] == 'span'
    try:
        shared.unpointed(text)
    except ValueError:
        assert pointed
    else:
        assert not pointed

report = {'result': 'pass', 'files': results, 'helper_codepoint_cases': 112, 'limits': 'Sparse AST/markup/codepoint checks only; constructors doubled. No project imports, real generators, project tests, visual QA, or live-source research.'}
(ROOT / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
