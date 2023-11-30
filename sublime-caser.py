import regex as re
import sublime
import sublime_plugin

EDGE_RE = re.compile(r"""
    # ABBRCamelCase
    \p{Lu}+(?=\p{Lu}\p{Ll})
    # CamelCase
    |\p{Lu}+[\p{Ll}\d]*
    # Other cases
    |[\p{Ll}\d]+
""", re.VERBOSE)

class Words(list):
    @classmethod
    def from_str(cls, src):
        return cls(val.group() for val in EDGE_RE.finditer(src))

    def lower(self):    return self.map(lower)
    def upper(self):    return self.map(upper)
    def title(self):    return self.map(title)
    def sentence(self): return self.lower().map_head(title)
    def initials(self): return self.map(initial)

    def spaced(self): return " ".join(self)
    def snake(self):  return "_".join(self)
    def kebab(self):  return "-".join(self)
    def solid(self):  return "".join(self)

    def camel(self):       return self.map_head(norm).map_tail(title).solid()
    def camel_lower(self): return self.title().map_head(lower).solid()
    def camel_title(self): return self.title().solid()

    def map(self, fun):
        for ind in range(len(self)):
            self[ind] = fun(self[ind])
        return self

    def map_head(self, fun):
        if len(self) > 0:
            self[0] = fun(self[0])
        return self

    def map_tail(self, fun):
        for ind in range(1, len(self)):
            self[ind] = fun(self[ind])
        return self

def lower(val): return val.lower()
def title(val): return val.title()
def upper(val): return val.upper()
def norm(val):  return val[0] + val[1:].lower()

def to_spaced(val):       return Words.from_str(val).spaced()
def to_spaced_lower(val): return Words.from_str(val).lower().spaced()
def to_spaced_title(val): return Words.from_str(val).title().spaced()
def to_spaced_upper(val): return Words.from_str(val).upper().spaced()

def to_camel(val):       return Words.from_str(val).camel()
def to_camel_lower(val): return Words.from_str(val).camel_lower()
def to_camel_title(val): return Words.from_str(val).camel_title()

def to_snake(val):       return Words.from_str(val).snake()
def to_snake_lower(val): return Words.from_str(val).lower().snake()
def to_snake_title(val): return Words.from_str(val).title().snake()
def to_snake_upper(val): return Words.from_str(val).upper().snake()

def to_kebab(val):       return Words.from_str(val).kebab()
def to_kebab_lower(val): return Words.from_str(val).lower().kebab()
def to_kebab_title(val): return Words.from_str(val).title().kebab()
def to_kebab_upper(val): return Words.from_str(val).upper().kebab()

def to_initials(val):       return Words.from_str(val).initials().solid()
def to_initials_lower(val): return Words.from_str(val).initials().lower().solid()
def to_initials_upper(val): return Words.from_str(val).initials().upper().solid()

def replace_by(view, edit, fun):
    for region in view.sel():
        if region.empty():
            continue
        view.replace(edit, region, fun(view.substr(region)))

def to_case(val, typ):
    if typ == "sentence_lower":
        return to_spaced_lower(val)
    if typ == "sentence_title":
        return to_spaced_title(val)
    if typ == "sentence_upper":
        return to_spaced_upper(val)
    if typ == "camel_lower":
        return to_camel_lower(val)
    if typ == "camel_title":
        return to_camel_title(val)
    if typ == "snake_lower":
        return to_snake_lower(val)
    if typ == "snake_title":
        return to_snake_title(val)
    if typ == "snake_upper":
        return to_snake_upper(val)
    if typ == "kebab_lower":
        return to_kebab_lower(val)
    if typ == "kebab_title":
        return to_kebab_title(val)
    if typ == "kebab_upper":
        return to_kebab_upper(val)
    if typ == "initials_lower":
        return to_initials_lower(val)
    if typ == "initials_upper":
        return to_initials_upper(val)
    raise Exception("unknown case format {}".format(typ))

def cmd(name, fun):
    class cmd(sublime_plugin.TextCommand):
        def run(self, edit):
            replace_by(self.view, edit, fun)
    cmd.__name__ = name
    return cmd

caser_spaced         = cmd("caser_spaced",         to_spaced)
caser_spaced_lower   = cmd("caser_spaced_lower",   to_spaced_lower)
caser_spaced_title   = cmd("caser_spaced_title",   to_spaced_title)
caser_spaced_upper   = cmd("caser_spaced_upper",   to_spaced_upper)
caser_camel          = cmd("caser_camel",          to_camel)
caser_camel_lower    = cmd("caser_camel_lower",    to_camel_lower)
caser_camel_title    = cmd("caser_camel_title",    to_camel_title)
caser_snake          = cmd("caser_snake",          to_snake)
caser_snake_lower    = cmd("caser_snake_lower",    to_snake_lower)
caser_snake_title    = cmd("caser_snake_title",    to_snake_title)
caser_snake_upper    = cmd("caser_snake_upper",    to_snake_upper)
caser_kebab          = cmd("caser_kebab",          to_kebab)
caser_kebab_lower    = cmd("caser_kebab_lower",    to_kebab_lower)
caser_kebab_title    = cmd("caser_kebab_title",    to_kebab_title)
caser_kebab_upper    = cmd("caser_kebab_upper",    to_kebab_upper)
caser_initials       = cmd("caser_initials",       to_initials)
caser_initials_lower = cmd("caser_initials_lower", to_initials_lower)
caser_initials_upper = cmd("caser_initials_upper", to_initials_upper)

class caser_go_tag(sublime_plugin.TextCommand):
    def run(self, edit, tags):
        view = self.view
        for region in view.sel():
            if region.empty():
                continue
            view.replace(edit, region, go_tags(view.substr(region), tags))

def go_tags(src, tags):
    return " ".join(go_tag(src, **tag) for tag in tags)

def go_tag(src, tag, case, omitempty = False):
    return tag + ":" + sublime.encode_value(go_tag_value(src, case, omitempty))

def go_tag_value(src, case, omitempty = False):
    src = to_case(src, case)
    if omitempty:
        return src + ",omitempty"
    return src
