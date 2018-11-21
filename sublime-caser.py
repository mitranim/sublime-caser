import re
import sublime_plugin


EDGE_RE = re.compile(r'''
    [A-Z0-9]+(?=\W|_|$)
    |
    [A-Z][a-z0-9]*(?=[A-Z]|\W|_|$)
    |
    [a-z0-9]+(?=[A-Z]|\W|_|$)
    |
    [A-Z0-9]+(?=[a-z]|\W|_|$)
    |
    [A-Za-z0-9]+(?=\W|_|$)
''', re.VERBOSE)


def to_lower_sentence_case(text): return ' '.join(m.group().lower() for m in EDGE_RE.finditer(text))
def to_title_sentence_case(text): return ' '.join(m.group().title() for m in EDGE_RE.finditer(text))
def to_upper_sentence_case(text): return ' '.join(m.group().upper() for m in EDGE_RE.finditer(text))

def to_lower_camel_case(text):
    words = EDGE_RE.findall(text)
    if len(words) < 1:
        return ''
    words[0] = words[0].lower()
    i = 1
    while i < len(words):
        words[i] = words[i].title()
        i += 1
    return ''.join(words)

def to_title_camel_case(text): return ''.join(m.group().title() for m in EDGE_RE.finditer(text))
def to_lower_snake_case(text): return '_'.join(m.group().lower() for m in EDGE_RE.finditer(text))
def to_title_snake_case(text): return '_'.join(m.group().title() for m in EDGE_RE.finditer(text))
def to_upper_snake_case(text): return '_'.join(m.group().upper() for m in EDGE_RE.finditer(text))
def to_lower_kebab_case(text): return '-'.join(m.group().lower() for m in EDGE_RE.finditer(text))
def to_title_kebab_case(text): return '-'.join(m.group().title() for m in EDGE_RE.finditer(text))
def to_upper_kebab_case(text): return '-'.join(m.group().upper() for m in EDGE_RE.finditer(text))
def to_lower_initials(text):   return ''.join(m.group().lower()[0] for m in EDGE_RE.finditer(text))
def to_upper_initials(text):   return ''.join(m.group().upper()[0] for m in EDGE_RE.finditer(text))


def replace_by(view, edit, fun):
    for region in view.sel():
        view.replace(edit, region, fun(view.substr(region)))


def cmd(name, fun):
    class cmd(sublime_plugin.TextCommand):
        def run(self, edit):
            replace_by(self.view, edit, fun)
    cmd.__name__ = name
    return cmd


caser_lower_sentence_case = cmd('caser_lower_sentence_case', to_lower_sentence_case)
caser_title_sentence_case = cmd('caser_title_sentence_case', to_title_sentence_case)
caser_upper_sentence_case = cmd('caser_upper_sentence_case', to_upper_sentence_case)
caser_lower_camel_case    = cmd('caser_lower_camel_case',    to_lower_camel_case)
caser_title_camel_case    = cmd('caser_title_camel_case',    to_title_camel_case)
caser_lower_snake_case    = cmd('caser_lower_snake_case',    to_lower_snake_case)
caser_title_snake_case    = cmd('caser_title_snake_case',    to_title_snake_case)
caser_upper_snake_case    = cmd('caser_upper_snake_case',    to_upper_snake_case)
caser_lower_kebab_case    = cmd('caser_lower_kebab_case',    to_lower_kebab_case)
caser_title_kebab_case    = cmd('caser_title_kebab_case',    to_title_kebab_case)
caser_upper_kebab_case    = cmd('caser_upper_kebab_case',    to_upper_kebab_case)
caser_lower_initials      = cmd('caser_lower_initials',      to_lower_initials)
caser_upper_initials      = cmd('caser_upper_initials',      to_upper_initials)
