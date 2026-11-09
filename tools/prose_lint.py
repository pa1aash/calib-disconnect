#!/usr/bin/env python3
"""Prose linter for academic LaTeX (and plain text or Markdown) manuscripts.

Usage:
    python3 tools/prose_lint.py PATH [--mode latex|text|auto] [--config CFG.toml]
                                     [--json OUT.json] [--md OUT.md] [--quiet]

Exit codes: 0 when no HARD finding exists, 1 when at least one HARD finding
exists, 2 on usage or configuration errors.

How it works
------------
1. LaTeX mode builds a "prose view" of the file: a string of the same length as
   the source in which every non-prose character (comments, math, verbatim,
   command names, reference and citation arguments, preamble) is replaced by a
   space. Newlines are kept, so offsets, line numbers, and columns of the
   original file are preserved exactly.
2. Structures are extracted from the source: the title, headings, captions, and
   paragraphs. Each becomes a "segment" (a slice of the prose view).
3. Rules run per segment and per sentence. Findings always report the line of
   the original file and the full original source line.

Design decisions
----------------
* Cross-reference placeholders: the argument of \\ref, \\eqref, and \\pageref is
  replaced by the single letter "N" so that "Section~\\ref{sec:x} shows" is seen
  as "Section N shows". For \\autoref, \\cref, and \\Cref the label prefix picks
  a word (sec: gives "Section N", tab: gives "Table N", fig: gives "Figure N").
  "\\S" becomes the section sign.
* \\item is replaced by a period-like sentence break so list items without
  terminal punctuation do not merge into one sentence.
* "real" is not in the softening-adverb list (see prose_lint.toml); "really" is.
  "rather" is not counted as a softener inside "rather than", and the word
  right after "rather than" is not counted either.
* Questions (sentences ending in "?") are not flagged by cleft_what.
* A one-sentence paragraph is never flagged by short_paragraph_end (configurable),
  and neither is a paragraph whose last sentence ends with a colon.
* A short final sentence is not flagged inside itemize, enumerate, or description
  lists, because list items are naturally short.
* internal_label skips tokens directly after a hyphen (DeepSeek-V3) or before a
  ".digit" tail (V3.1), which are model or version names; letter-digit codes
  such as C1, L2, B1, or W3 still fire. The allowlist covers hardware and metrics.
* mc_precision considers only numbers with a decimal point or exponent, because an
  integer such as a resample count is not a precision claim.
* pvalue_precision and mc_precision read the source with comments and verbatim
  blanked but math kept, since p-values usually sit in math.
* Tabular environments are separate "table" segments. They are scanned only by
  decimal_in_prose, and only when options.decimal_skip_tables is false.
* The abbreviation-aware sentence splitter does not break after common
  abbreviations (e.g., i.e., et al., Fig., Eq., Sec., vs., cf., single capital
  initials) or inside decimals, and does not break when the next word is
  lowercase. "etc." followed by a capital letter does break.
"""

from __future__ import annotations

import argparse
import bisect
import json
import re
import sys
import tomllib
from dataclasses import dataclass, asdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = SCRIPT_DIR / "prose_lint.toml"

CATEGORIES = [
    "negation_not_but", "negation_cascade", "rather_than", "significance_announcer",
    "significantly", "negation_comma_not", "roadmap", "softening_adverb", "contradictory_pair",
    "cleft_what", "cleft_it_that", "cleft_there_which", "heading", "caption_length",
    "short_paragraph_end", "internal_label", "process_word", "file_path",
    "underscore_identifier", "decimal_in_prose", "pvalue_precision", "mc_precision",
    "british_spelling", "em_dash", "title",
]

CAT_DESCRIPTIONS = {
    "negation_not_but": "Rhetorical 'not X but Y' and variants",
    "negation_cascade": "Three or more consecutive rule-out sentences",
    "rather_than": "'rather than' construction",
    "significance_announcer": "Sentence announces its own significance",
    "significantly": "'significantly' used as a sentence adverb",
    "negation_comma_not": "Comma contrast ', not X'",
    "roadmap": "Roadmap or forward-pointer phrase",
    "softening_adverb": "Softening adverb",
    "contradictory_pair": "Contradictory hedge pair",
    "cleft_what": "Sentence starting with 'What'",
    "cleft_it_that": "'It is X that' cleft",
    "cleft_there_which": "'There is X which' expletive",
    "heading": "Heading style (colon, question, list, suffix)",
    "caption_length": "Caption too long",
    "short_paragraph_end": "Paragraph ends on a very short sentence",
    "internal_label": "Internal tracking label such as C1 or L2",
    "process_word": "Process-record word (session, wave, gate)",
    "file_path": "File name or path in prose",
    "underscore_identifier": "Code identifier with underscore in prose",
    "decimal_in_prose": "Decimal numeral in prose",
    "pvalue_precision": "p-value with too many significant figures",
    "mc_precision": "Monte Carlo number with too many significant figures",
    "british_spelling": "British spelling",
    "em_dash": "Em-dash",
    "title": "Title contains ':' or '?'",
}

MATH_ENVS = {
    "equation", "align", "gather", "multline", "eqnarray", "math", "displaymath",
    "flalign", "alignat", "split",
}
MATH_ENVS |= {e + "*" for e in list(MATH_ENVS)}

# Environments that are cut out of paragraph text (captions are still read).
CUT_ENVS = {
    "figure", "figure*", "table", "table*", "algorithm", "algorithm*",
    "thebibliography", "wrapfigure", "sidewaystable", "sidewaysfigure",
    "tabular", "tabular*", "tabularx", "longtable",
}
LIST_ENVS = {"itemize", "enumerate", "description"}
TABULAR_ENVS = {"tabular", "tabular*", "tabularx", "longtable"}
# Braced arguments to blank right after \begin{env}.
ENV_ARGN = {"tabular": 1, "tabular*": 2, "tabularx": 2, "longtable": 1, "array": 1,
            "minipage": 1, "wrapfigure": 2, "multicols": 1}

REF_PLAIN = {"ref", "eqref", "pageref", "nameref"}
REF_WORDED = {"autoref", "cref", "Cref", "vref", "Vref", "cpageref"}

# Commands whose leading braced arguments are blanked (name -> count).
BLANK_ARGS = {
    "cite": 1, "citet": 1, "citep": 1, "citeauthor": 1, "citeyear": 1, "citealp": 1,
    "citealt": 1, "citeyearpar": 1, "Citet": 1, "Citep": 1, "parencite": 1,
    "textcite": 1, "autocite": 1, "nocite": 1, "label": 1, "url": 1,
    "includegraphics": 1, "input": 1, "include": 1, "bibliography": 1,
    "bibliographystyle": 1, "usepackage": 1, "RequirePackage": 1, "documentclass": 1,
    "hspace": 1, "vspace": 1, "textcolor": 1, "color": 1, "resizebox": 2,
    "scalebox": 1, "setlength": 2, "setcounter": 2, "addtocounter": 2,
    "pagestyle": 1, "thispagestyle": 1, "author": 1, "date": 1, "email": 1,
    "address": 1, "addr": 1, "bibitem": 1, "index": 1, "hyperref": 0, "pagecolor": 1,
}
HEADING_CMDS = {"section", "subsection", "subsubsection", "paragraph", "subparagraph",
                "chapter", "part"}
NEWCMD = {"newcommand": 1, "renewcommand": 1, "providecommand": 1,
          "DeclareMathOperator": 1, "newenvironment": 2, "renewenvironment": 2}

NAME_RE = re.compile(r"\\([A-Za-z@]+)(\*?)")
BEGIN_VERB_RE = re.compile(r"\\begin\s*\{(verbatim\*?|Verbatim\*?|lstlisting|minted|comment)\}")
VERB_RE = re.compile(r"\\verb\*?([^A-Za-z\s*])")
URL_RE = re.compile(r"https?://[^\s{}]+")
BLANK_LINE_RE = re.compile(r"\n[ \t]*\n")
DIMENSION_RE = re.compile(
    r"[ \t]*=?\s*[-+]?(?:\d+\.?\d*|\.\d+)\s*(?:pt|in|cm|mm|em|ex|bp|pc|sp|mu|truein)\b"
    r"(?:\s*(?:plus|minus)\s*[-+]?(?:\d+\.?\d*|\.\d+)\s*(?:pt|in|cm|mm|em|ex|fil+))*")

ABBREV = {
    "e.g", "i.e", "al", "fig", "figs", "eq", "eqs", "sec", "secs", "vs", "cf", "etc",
    "approx", "resp", "no", "nos", "dr", "mr", "mrs", "ms", "prof", "ref", "refs",
    "tab", "viz", "ca", "st", "cf", "thm", "lem", "prop", "def", "vol", "pp", "ch",
}

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def match_brace(s: str, i: int, hi: int) -> int:
    """Return the index of the brace matching s[i] == '{', or -1."""
    depth = 0
    j = i
    while j < hi:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return -1


def count_words(text: str) -> int:
    return sum(1 for w in text.split() if re.search(r"\w", w))


def collapse(text: str, limit: int = 100) -> str:
    t = " ".join(text.split())
    return t if len(t) <= limit else t[: limit - 3] + "..."


SENT_TERM = re.compile(r"([.!?]+)([\"'\u2019\u201d)\]]*)(?=\s|$)")
NEXT_CHAR = re.compile(r"\s*(\S)")


def split_sentences(text: str) -> list[tuple[int, int]]:
    """Return (start, end) spans of sentences in text, abbreviation aware."""
    spans: list[tuple[int, int]] = []
    start = 0
    n = len(text)
    for m in SENT_TERM.finditer(text):
        p = m.start(1)
        term = m.group(1)
        end = m.end()
        nm = NEXT_CHAR.match(text, end)
        if not nm:
            continue
        nc = nm.group(1)
        if term == ".":
            prev = text[p - 1] if p > 0 else " "
            if prev.isspace():
                brk = True
            else:
                tok = re.search(r"([A-Za-z][A-Za-z.]*)$", text[max(0, p - 20):p])
                word = tok.group(1) if tok else ""
                low = word.lower()
                if low in ABBREV:
                    brk = low == "etc" and nc.isupper()
                elif len(word) == 1 and word.isupper():
                    brk = False
                else:
                    brk = not nc.islower()
        elif term.startswith("."):
            brk = nc.isupper()
        else:
            brk = not nc.islower()
        if brk:
            spans.append((start, end))
            start = end
    spans.append((start, n))
    out = []
    for a, b in spans:
        seg = text[a:b]
        lead = len(seg) - len(seg.lstrip())
        a2, b2 = a + lead, a + len(seg.rstrip())
        if re.search(r"[A-Za-z0-9]", text[a2:b2]):
            out.append((a2, b2))
    return out


def sig_figs(num: str) -> int:
    m = re.match(r"\s*(\d+(?:\.\d*)?|\.\d+)", num)
    if not m:
        return 0
    mant = m.group(1)
    if "." in mant:
        digits = mant.replace(".", "").lstrip("0")
    else:
        digits = mant.lstrip("0").rstrip("0")
    return len(digits)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    file: str
    line: int
    col: int
    category: str
    severity: str
    match: str
    source_line: str
    message: str = ""


@dataclass
class Segment:
    kind: str  # title, heading, caption, paragraph, table
    a: int
    b: int


# ---------------------------------------------------------------------------
# LaTeX stripping
# ---------------------------------------------------------------------------


def blank_comments_and_verbatim(raw: str) -> str:
    """Blank comments, verbatim-like environments, and \\verb, keeping newlines."""
    out = list(raw)
    n = len(raw)

    def blank(a: int, b: int) -> None:
        for k in range(a, min(b, n)):
            if out[k] != "\n":
                out[k] = " "

    i = 0
    while i < n:
        c = raw[i]
        if c == "\\":
            m = BEGIN_VERB_RE.match(raw, i)
            if m:
                env = m.group(1)
                endtok = "\\end{" + env + "}"
                j = raw.find(endtok, m.end())
                e = n if j == -1 else j + len(endtok)
                blank(i, e)
                i = e
                continue
            m = VERB_RE.match(raw, i)
            if m:
                d = m.group(1)
                j = raw.find(d, m.end())
                eol = raw.find("\n", m.end())
                eol = n if eol == -1 else eol
                e = eol if (j == -1 or j > eol) else j + 1
                blank(i, e)
                i = e
                continue
            i += 2
            continue
        if c == "%":
            j = raw.find("\n", i)
            j = n if j == -1 else j
            blank(i, j)
            i = j
            continue
        i += 1
    return "".join(out)


class LatexView:
    """Builds the prose view and extracts structures from comment-free source."""

    def __init__(self, raw: str, cfg: dict):
        self.raw = raw
        self.clean = blank_comments_and_verbatim(raw)
        self.s = self.clean
        self.n = len(raw)
        self.out = list(self.clean)
        lists = cfg.get("lists", {})
        self.number_macros = set(lists.get("number_macros", []))
        self.code_macros = set(lists.get("code_macros", ["texttt"]))
        self.title_macros = set(lists.get("title_macros", ["title"]))
        self.titles: list[tuple[int, int]] = []
        self.code_spans: list[tuple[int, int]] = []
        self.number_spans: list[tuple[int, int]] = []
        self.table_spans: list[tuple[int, int]] = []
        self.list_spans: list[tuple[int, int]] = []
        self.cuts: list[tuple[int, int]] = []
        self.headings: list[tuple[int, int]] = []
        self.captions: list[tuple[int, int]] = []
        self.title: tuple[int, int] | None = None
        self.body_start = 0
        self.body_end = self.n
        self._build()

    # -- low-level helpers -------------------------------------------------
    def blank(self, a: int, b: int) -> None:
        out = self.out
        for k in range(a, min(b, self.n)):
            if out[k] != "\n":
                out[k] = " "

    def args(self, pos: int, nbraced: int, hi: int) -> int:
        """End index after optional [..] groups (before the first brace) and
        nbraced braced groups, starting at pos. Only spaces and tabs are skipped."""
        s = self.s
        done = 0
        j = pos
        while True:
            k = j
            while k < hi and s[k] in " \t":
                k += 1
            if k >= hi:
                break
            ch = s[k]
            if ch == "[" and done == 0:
                e = s.find("]", k, hi)
                if e == -1 or "\n\n" in s[k:e]:
                    break
                j = e + 1
                continue
            if ch == "{" and done < nbraced:
                e = match_brace(s, k, hi)
                if e == -1:
                    break
                j = e + 1
                done += 1
                if done == nbraced:
                    break
                continue
            break
        return j

    def find_end(self, env: str, pos: int, hi: int) -> tuple[int, int] | None:
        rx = re.compile(r"\\(begin|end)\s*\{" + re.escape(env) + r"\}")
        depth = 1
        for m in rx.finditer(self.s, pos, hi):
            depth += 1 if m.group(1) == "begin" else -1
            if depth == 0:
                return m.start(), m.end()
        return None

    # -- main build --------------------------------------------------------
    def _build(self) -> None:
        s = self.s
        m = re.search(r"\\begin\s*\{document\}", s)
        if m:
            self.body_start = m.end()
            e = re.search(r"\\end\s*\{document\}", s[self.body_start:])
            self.body_end = self.body_start + e.start() if e else self.n
            # title in the preamble
            alt = "|".join(re.escape(t) for t in sorted(self.title_macros, key=len, reverse=True))
            if alt:
                trx = re.compile(r"\\(?:" + alt + r")\*?\s*(?:\[[^\]]*\])?\s*\{")
                for tm in trx.finditer(s, 0, m.start()):
                    k = tm.end() - 1
                    ee = match_brace(s, k, m.start())
                    if ee != -1:
                        self.titles.append((k + 1, ee))
                        self.scan(k, ee + 1)
        self.scan(self.body_start, self.body_end)
        if m:
            prev = 0
            for ta, tb in sorted(self.titles):
                if ta >= prev:
                    self.blank(prev, ta)
                    prev = tb
            self.blank(prev, self.body_start)
            self.blank(self.body_end, self.n)
            self.cuts.append((0, self.body_start))
            self.cuts.append((self.body_end, self.n))
        self.title = self.titles[0] if self.titles else None
        # bare URLs
        text = "".join(self.out)
        for um in URL_RE.finditer(text):
            self.blank(um.start(), um.end())
        self.view = "".join(self.out)

    def scan(self, lo: int, hi: int) -> None:
        s = self.s
        out = self.out
        i = lo
        while i < hi:
            c = s[i]
            if c == "\\":
                i = self.command(i, hi)
            elif c == "$":
                i = self.dollar(i, hi)
            elif c in "{}~":
                out[i] = " "
                i += 1
            else:
                i += 1

    def dollar(self, i: int, hi: int) -> int:
        s = self.s
        if i + 1 < hi and s[i + 1] == "$":
            j = s.find("$$", i + 2, hi)
            width = 2
        else:
            width = 1
            j = -1
            k = i + 1
            while k < hi:
                if s[k] == "\\":
                    k += 2
                    continue
                if s[k] == "$":
                    j = k
                    break
                k += 1
        if j == -1 or BLANK_LINE_RE.search(s, i, j):
            self.blank(i, i + width)
            return i + width
        self.blank(i, j + width)
        return j + width

    def command(self, i: int, hi: int) -> int:
        s = self.s
        out = self.out
        nxt = s[i + 1] if i + 1 < hi else ""
        if nxt == "":
            return i + 1
        if nxt in "([":
            closer = ")" if nxt == "(" else "]"
            j = s.find("\\" + closer, i + 2, hi)
            if j == -1:
                self.blank(i, i + 2)
                return i + 2
            self.blank(i, j + 2)
            return j + 2
        if nxt == "\\":
            self.blank(i, i + 2)
            j = i + 2
            mo = re.compile(r"\*?\s*\[[^\]\n]*\]").match(s, j, hi)
            if mo:
                self.blank(j, mo.end())
                return mo.end()
            return j
        if nxt == "_":
            return i + 2
        if nxt == "%":
            out[i] = " "
            return i + 2
        if not nxt.isalpha():
            self.blank(i, i + 2)
            return i + 2
        m = NAME_RE.match(s, i)
        name = m.group(1)
        j = m.end()
        # -- environments
        if name in ("begin", "end"):
            mo = re.compile(r"\s*\{([^{}]*)\}").match(s, j, hi)
            if not mo:
                self.blank(i, j)
                return j
            env = mo.group(1).strip()
            endpos = mo.end()
            if name == "end":
                self.blank(i, endpos)
                return endpos
            if env in MATH_ENVS:
                fe = self.find_end(env, endpos, hi)
                if fe is None:
                    self.blank(i, endpos)
                    return endpos
                self.blank(i, fe[1])
                return fe[1]
            self.blank(i, endpos)
            k = self.args(endpos, ENV_ARGN.get(env, 0), hi)
            self.blank(endpos, k)
            if env in LIST_ENVS:
                fe = self.find_end(env, k, hi)
                self.list_spans.append((i, fe[1] if fe else hi))
            if env in CUT_ENVS:
                fe = self.find_end(env, k, hi)
                self.cuts.append((i, fe[1] if fe else hi))
                if env in TABULAR_ENVS and fe:
                    self.table_spans.append((k, fe[0]))
            return k
        # -- cross references
        if name in REF_PLAIN or name in REF_WORDED:
            k = j
            while k < hi and s[k] in " \t":
                k += 1
            if k < hi and s[k] == "{":
                e = match_brace(s, k, hi)
                if e != -1:
                    text = "N"
                    if name in REF_WORDED:
                        label = s[k + 1:e].split(":")[0].strip().lower()
                        words = {
                            "sec": "Section N", "subsec": "Section N", "ssec": "Section N",
                            "app": "Section N", "appendix": "Section N", "section": "Section N",
                            "tab": "Table N", "table": "Table N",
                            "fig": "Figure N", "figure": "Figure N",
                        }
                        text = words.get(label, "N")
                    width = e + 1 - i
                    if len(text) > width:
                        text = "N"
                    self.blank(i, e + 1)
                    for off, ch in enumerate(text):
                        out[i + off] = ch
                    return e + 1
            self.blank(i, j)
            return j
        if name == "S" and not m.group(2):
            self.blank(i, j)
            out[i] = "\u00a7"
            return j
        if name == "item":
            self.blank(i, j)
            out[j - 1] = "."
            return j
        if name == "textemdash":
            self.blank(i, j)
            out[i:i + 3] = list("---")
            return j
        if name == "href":
            k = j
            if k < hi and s[k] == "{":
                e = match_brace(s, k, hi)
                if e != -1:
                    self.blank(i, e + 1)
                    return e + 1
            self.blank(i, j)
            return j
        if name in self.number_macros:
            self.blank(i, j)
            nargs = 2 if name == "SI" else 1
            k = self.args(j, 0, hi)
            self.blank(j, k)
            for _ in range(nargs):
                q = k
                while q < hi and s[q] in " \t":
                    q += 1
                if q < hi and s[q] == "{":
                    e = match_brace(s, q, hi)
                    if e == -1:
                        break
                    self.blank(q, q + 1)
                    self.blank(e, e + 1)
                    self.number_spans.append((q + 1, e))
                    k = e + 1
                else:
                    break
            return k
        if name in self.code_macros:
            self.blank(i, j)
            k = j
            while k < hi and s[k] in " \t":
                k += 1
            if k < hi and s[k] == "{":
                e = match_brace(s, k, hi)
                if e != -1:
                    self.code_spans.append((k + 1, e))
            return j
        if name in HEADING_CMDS or name in ("caption", "captionof", "subcaption") or name in self.title_macros:
            self.blank(i, j)
            k = j
            if name == "captionof":
                k = self.args(j, 1, hi)
                self.blank(j, k)
            else:
                k = self.args(j, 0, hi)
                self.blank(j, k)
            q = k
            while q < hi and s[q] in " \t\n":
                q += 1
            if q < hi and s[q] == "{":
                e = match_brace(s, q, hi)
                if e != -1:
                    if name in HEADING_CMDS:
                        self.headings.append((q + 1, e))
                    elif name in self.title_macros:
                        if (q + 1, e) not in self.titles:
                            self.titles.append((q + 1, e))
                    else:
                        self.captions.append((q + 1, e))
                    self.cuts.append((i, e + 1))
                    return q
            return k
        if name in NEWCMD:
            self.blank(i, j)
            k = j
            while k < hi and s[k] in " \t":
                k += 1
            if k < hi and s[k] == "{":
                e = match_brace(s, k, hi)
                k = (e + 1) if e != -1 else k + 1
            elif k < hi and s[k] == "\\":
                mo = NAME_RE.match(s, k)
                k = mo.end() if mo else k + 2
            bodies = NEWCMD[name]
            while True:
                q = k
                while q < hi and s[q] in " \t":
                    q += 1
                if q < hi and s[q] == "[":
                    e = s.find("]", q, hi)
                    if e == -1:
                        break
                    k = e + 1
                elif q < hi and s[q] == "{" and bodies > 0:
                    e = match_brace(s, q, hi)
                    if e == -1:
                        break
                    k = e + 1
                    bodies -= 1
                else:
                    break
            self.blank(j, k)
            return k
        if name == "def":
            self.blank(i, j)
            q = s.find("{", j, hi)
            if q != -1 and "\n\n" not in s[j:q]:
                e = match_brace(s, q, hi)
                if e != -1:
                    self.blank(j, e + 1)
                    return e + 1
            return j
        if name in BLANK_ARGS:
            k = self.args(j, BLANK_ARGS[name], hi)
            self.blank(i, k)
            return k
        # unknown command: blank its name and a trailing TeX dimension (\vskip 0.3in)
        self.blank(i, j)
        dm = DIMENSION_RE.match(s, j, hi)
        if dm:
            self.blank(j, dm.end())
            return dm.end()
        return j


# ---------------------------------------------------------------------------
# Text (Markdown or plain) view
# ---------------------------------------------------------------------------

HEADING_MD_RE = re.compile(r"^(\s*)(#{1,6})\s+(.*?)\s*#*\s*$")
CAPTION_TXT_RE = re.compile(
    r"^\s*(?:(?:Figure|Fig\.|Table)\s+\d+[A-Za-z]?\s*[:.]|Caption\s*:)\s*", re.I)
BACKTICK_RE = re.compile(r"`([^`\n]+)`")


class TextView:
    def __init__(self, raw: str, cfg: dict):
        self.raw = raw
        self.clean = raw
        out = list(raw)
        for um in URL_RE.finditer(raw):
            for k in range(um.start(), um.end()):
                out[k] = " "
        self.view = "".join(out)
        self.code_spans = [(m.start(1), m.end(1)) for m in BACKTICK_RE.finditer(raw)]
        self.number_spans: list[tuple[int, int]] = []
        self.table_spans: list[tuple[int, int]] = []
        self.list_spans: list[tuple[int, int]] = []
        self.cuts: list[tuple[int, int]] = []
        self.headings: list[tuple[int, int]] = []
        self.captions: list[tuple[int, int]] = []
        self.title: tuple[int, int] | None = None
        self.titles: list[tuple[int, int]] = []
        self.body_start = 0
        self.body_end = len(raw)
        pos = 0
        lines = raw.split("\n")
        k = 0
        while k < len(lines):
            line = lines[k]
            ls = pos
            le = pos + len(line)
            hm = HEADING_MD_RE.match(line)
            cm = CAPTION_TXT_RE.match(line)
            if hm:
                a = ls + hm.start(3)
                b = ls + hm.end(3)
                if len(hm.group(2)) == 1 and self.title is None:
                    self.title = (a, b)
                    self.titles.append((a, b))
                else:
                    self.headings.append((a, b))
                self.cuts.append((ls, le))
            elif cm:
                a = ls + cm.end()
                end_line = k
                bend = le
                p2 = le + 1
                while end_line + 1 < len(lines):
                    nl = lines[end_line + 1]
                    if not nl.strip() or HEADING_MD_RE.match(nl):
                        break
                    end_line += 1
                    bend = p2 + len(nl)
                    p2 = bend + 1
                self.captions.append((a, bend))
                self.cuts.append((ls, bend))
                pos = bend + 1
                k = end_line + 1
                continue
            pos = le + 1
            k += 1


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def load_config(path: Path) -> dict:
    with open(path, "rb") as fh:
        cfg = tomllib.load(fh)
    sev = cfg.get("severity", {})
    for cat in CATEGORIES:
        v = str(sev.get(cat, "HARD")).upper()
        if v not in ("HARD", "WARN", "OFF"):
            raise ValueError(f"invalid severity {v!r} for category {cat}")
        sev[cat] = v
    cfg["severity"] = sev
    return cfg


def phrase_regex(phrases: list[str]) -> re.Pattern | None:
    if not phrases:
        return None
    parts = sorted(phrases, key=len, reverse=True)
    body = "|".join(re.escape(p).replace(r"\ ", r"\s+") for p in parts)
    return re.compile(r"\b(?:" + body + r")\b", re.I)


# ---------------------------------------------------------------------------
# Linter
# ---------------------------------------------------------------------------

NOT_BUT_PATTERNS = [
    re.compile(r"\bnot\s+(?:merely|simply)\b", re.I),
    re.compile(r"\bnot\s+(?:only|just)\b.*?\bbut\b", re.I | re.S),
    re.compile(r"\bnot\b.{0,300}?,\s*not\b.{0,300}?,?\s*but\b", re.I | re.S),
    re.compile(r"\bnot\b(?:\s+\S+){0,12}?\s+but\b", re.I),
]
NEG_RE = re.compile(r"\b(?:not|no|neither|nor|never|cannot)\b|n[\u2019']t\b", re.I)
UNDERSCORE_RE = re.compile(r"[A-Za-z0-9]+(?:\\?_[A-Za-z0-9]+)+")
# Not preceded by a hyphen (DeepSeek-V3) and not followed by ".digit" (V3.1).
INTERNAL_RE = re.compile(r"(?<![-\w])[A-Z]{1,2}\d{1,2}[a-z]?\b(?![.]\d)")
DECIMAL_RE = re.compile(r"(?<![\w.\u00a7])(?:\d+\.\d+(?!\.?\d)|\.\d+)")
EMDASH_RE = re.compile("[\u2014\u2015]|(?<!-)---(?!-)")
CLEFT_WHAT_RE = re.compile(r"\W*(What)\b")
CLEFT_IT_RE = re.compile(r"\W*(It\s+(?:is|was)\s+)((?:[\w'\u2019\-,]+\s+){0,8}?)that\b")
CLEFT_THERE_RE = re.compile(
    r"\W*(There\s+(?:is|are|was|were|exists?)\s+)((?:[\w'\u2019\-,]+\s+){0,8}?)(?:which|that|who)\b")

_NUM = r"(?:\d+(?:\.\d*)?|\.\d+)"
_EXP = (r"(?:\s*[eE][+\-\u2212]?\d+|\s*(?:\\times|\\cdot|\u00d7|x)\s*10\s*\^\s*\{?\s*"
        r"[+\-\u2212]?\s*\d+\s*\}?)")
_NUMEXP = _NUM + _EXP + "?"
_SEP = r"(?:\s|~|\\[,;:! ]|\{|\})*"
_OP = (r"(?:<=|>=|=|<|>|\\leq?|\\geq?|\\le|\\ge|\u2264|\u2265|\\approx|\u2248|"
       r"\\lesssim|\\sim|\\lt|\\gt)")
P_EQ_RE = re.compile(
    r"(?<![A-Za-z\\])[pP](?:_\{[^{}]*\}|_[A-Za-z0-9])?" + _SEP + _OP + _SEP
    + r"(?P<n>" + _NUMEXP + ")")
P_WORD_RE = re.compile(
    r"(?<![A-Za-z])p\$?[\s~\-]*values?\$?(?:\s|~)*"
    r"(?:(?:of|is|was|equals?|equal\s+to|at|near|around|about|reaches?)\b|" + _OP + ")?"
    + _SEP + r"(?P<n>" + _NUMEXP + ")", re.I)
MC_NUM_RE = re.compile(
    r"(?<![\w.])(?:(?:\d+\.\d+|\.\d+)(?:" + _EXP + r")?|\d+" + _EXP + ")")
MC_RE = re.compile(r"monte[\s\-]+carlo", re.I)


class Linter:
    def __init__(self, raw: str, mode: str, cfg: dict, filename: str = "<input>"):
        self.raw = raw
        self.mode = mode
        self.cfg = cfg
        self.filename = filename
        self.sev = cfg["severity"]
        th = cfg.get("thresholds", {})
        self.cap_sent = int(th.get("caption_max_sentences", 3))
        self.cap_words = int(th.get("caption_max_words", 60))
        self.short_words = int(th.get("short_paragraph_max_words", 8))
        self.casc_min = int(th.get("negation_cascade_min", 3))
        self.p_sig = int(th.get("pvalue_max_sigfigs", 2))
        opts = cfg.get("options", {})
        self.decimal_skip_tables = bool(opts.get("decimal_skip_tables", True))
        self.short_skip_single = bool(opts.get("short_paragraph_skip_single", True))
        lists = cfg.get("lists", {})
        self.view_obj = LatexView(raw, cfg) if mode == "latex" else TextView(raw, cfg)
        v = self.view_obj
        self.view = v.view
        self.clean = v.clean
        self.line_starts = [0]
        for m in re.finditer(r"\n", raw):
            self.line_starts.append(m.end())
        self.raw_lines = raw.split("\n")
        self.findings: list[Finding] = []

        adverbs = lists.get("softening_adverbs", [])
        alts = []
        for w in sorted(adverbs, key=len, reverse=True):
            alts.append(re.escape(w) + (r"(?!\s+than\b)" if w.lower() == "rather" else ""))
        self.rx_adverb = re.compile(r"\b(?:" + "|".join(alts) + r")\b", re.I) if alts else None
        self.rx_contra = phrase_regex(lists.get("contradictory_pairs", []))
        self.rx_signif = phrase_regex(lists.get("significance_phrases", []))
        ini = lists.get("significance_initial_phrases", [])
        self.rx_signif_init = None
        if ini:
            body = "|".join(re.escape(p).replace(r"\ ", r"\s+") for p in ini)
            self.rx_signif_init = re.compile(r"\W*(" + body + r")\b", re.I)
        excl = [re.escape(w) for w in lists.get("negation_comma_not_exclude", [])]
        ex = (r"(?!(?:" + "|".join(excl) + r")\b)") if excl else ""
        self.rx_comma_not = re.compile(r"(?<=\w),\s+not\s+" + ex + r"(?:a|an|the|[A-Za-z][\w\-]*)\b", re.I)
        self.rx_road = [re.compile(p, re.I | re.S) for p in lists.get("roadmap_phrases", [])]
        self.allow_labels = set(lists.get("internal_label_allowlist", []))
        self.rx_process = phrase_regex(lists.get("process_words", []))
        exts = lists.get("file_extensions", [])
        self.rx_file = None
        if exts:
            alt = "|".join(re.escape(e) for e in sorted(exts, key=len, reverse=True))
            self.rx_file = re.compile(
                r"(?<![\w/.\-])(?:[\w.\-]+/)*[\w\-]+(?:\.[\w\-]+)*\.(?:" + alt + r")(?![\w])",
                re.I)
        self.rx_abs_path = re.compile(
            r"(?<![\w/])/(?:home|usr|etc|var|tmp|opt|mnt|Users|scratch)/[\w./\-]+")
        self.exempt = {w.lower() for w in lists.get("decimal_context_exempt", [])}
        self.it_exclude = {w.lower() for w in lists.get("cleft_it_that_exclude", [])}
        brit = cfg.get("british_spellings", {})
        self.british = {k.lower(): v for k, v in brit.items()}
        self.rx_british = None
        if self.british:
            keys = sorted(self.british, key=len, reverse=True)
            self.rx_british = re.compile(
                r"\b(?:" + "|".join(re.escape(k) for k in keys) + r")\b", re.I)

    # -- reporting ---------------------------------------------------------
    def line_col(self, off: int) -> tuple[int, int]:
        idx = bisect.bisect_right(self.line_starts, off) - 1
        return idx + 1, off - self.line_starts[idx] + 1

    def emit(self, cat: str, a: int, b: int, message: str = "", text: str | None = None) -> None:
        sev = self.sev.get(cat, "HARD")
        if sev == "OFF":
            return
        line, col = self.line_col(a)
        src = self.raw_lines[line - 1].strip() if line - 1 < len(self.raw_lines) else ""
        if len(src) > 300:
            src = src[:297] + "..."
        if text is None:
            text = self.raw[a:b]
        self.findings.append(Finding(self.filename, line, col, cat, sev,
                                     collapse(text), src, message))

    @staticmethod
    def in_spans(pos: int, spans: list[tuple[int, int]]) -> bool:
        return any(a <= pos < b for a, b in spans)

    # -- segments ----------------------------------------------------------
    def segments(self) -> list[Segment]:
        v = self.view_obj
        segs: list[Segment] = []
        for ta, tb in v.titles:
            segs.append(Segment("title", ta, tb))
        for a, b in v.headings:
            segs.append(Segment("heading", a, b))
        for a, b in v.captions:
            segs.append(Segment("caption", a, b))
        for a, b in v.table_spans:
            segs.append(Segment("table", a, b))
        par = list("".join(self.view))
        n = len(par)
        for a, b in v.cuts:
            for k in range(max(0, a), min(b, n)):
                par[k] = "\x00"
        pos = 0
        for line in self.raw.split("\n"):
            if not line.strip():
                for k in range(pos, min(pos + len(line) + 1, n)):
                    par[k] = "\x00"
            pos += len(line) + 1
        text = "".join(par)
        for m in re.finditer(r"[^\x00]+", text):
            seg = self.view[m.start():m.end()]
            lead = len(seg) - len(seg.lstrip())
            a, b = m.start() + lead, m.start() + len(seg.rstrip())
            if re.search(r"[A-Za-z0-9]", self.view[a:b]):
                segs.append(Segment("paragraph", a, b))
        return segs

    # -- main --------------------------------------------------------------
    def run(self) -> list[Finding]:
        segs = self.segments()
        for seg in segs:
            self.process_segment(seg)
        self.check_headings()
        self.check_captions()
        self.check_title()
        self.check_precision()
        self.findings.sort(key=lambda f: (f.line, f.col, f.category))
        return self.findings

    def dedupe(self, hits: list[tuple[str, int, int, str]]) -> list[tuple[str, int, int, str]]:
        out = []
        taken: dict[str, list[tuple[int, int]]] = {}
        for cat, a, b, msg in sorted(hits, key=lambda h: (h[1], -(h[2] - h[1]))):
            if any(a < y and x < b for x, y in taken.get(cat, [])):
                continue
            taken.setdefault(cat, []).append((a, b))
            out.append((cat, a, b, msg))
        return out

    def process_segment(self, seg: Segment) -> None:
        text = self.view[seg.a:seg.b]
        base = seg.a
        hits: list[tuple[str, int, int, str]] = []
        v = self.view_obj

        # decimals (also for tables when allowed)
        if seg.kind == "table":
            if not self.decimal_skip_tables:
                self.rule_decimal(text, base, hits)
            for cat, a, b, msg in self.dedupe(hits):
                self.emit(cat, a, b, msg)
            return
        if seg.kind != "table":
            self.rule_decimal(text, base, hits)

        sents = split_sentences(text)
        for s, e in sents:
            self.sentence_rules(text[s:e], base + s, hits)

        # word-level rules on the whole segment
        for m in INTERNAL_RE.finditer(text):
            if m.group(0) not in self.allow_labels:
                hits.append(("internal_label", base + m.start(), base + m.end(), ""))
        if self.rx_process:
            for m in self.rx_process.finditer(text):
                hits.append(("process_word", base + m.start(), base + m.end(), ""))
        if self.rx_file:
            for m in self.rx_file.finditer(text):
                hits.append(("file_path", base + m.start(), base + m.end(), ""))
        for m in self.rx_abs_path.finditer(text):
            hits.append(("file_path", base + m.start(), base + m.end(), ""))
        for m in UNDERSCORE_RE.finditer(text):
            if not self.in_spans(base + m.start(), v.code_spans):
                hits.append(("underscore_identifier", base + m.start(), base + m.end(), ""))
        if self.rx_british:
            for m in self.rx_british.finditer(text):
                am = self.british[m.group(0).lower()]
                hits.append(("british_spelling", base + m.start(), base + m.end(),
                             f"American: {am}"))
        for m in EMDASH_RE.finditer(text):
            if self.mode == "text" and m.group(0) == "---":
                ls = text.rfind("\n", 0, m.start()) + 1
                le = text.find("\n", m.end())
                le = len(text) if le == -1 else le
                if not re.search(r"[A-Za-z0-9]", text[ls:le]):
                    continue
            hits.append(("em_dash", base + m.start(), base + m.end(), ""))

        if seg.kind == "paragraph":
            self.paragraph_rules(text, base, sents, hits)

        # cross-category suppression: softener inside a contradictory pair
        contra = [(a, b) for c, a, b, _ in hits
                  if c in ("contradictory_pair", "significance_announcer")]
        notbut = [(a, b) for c, a, b, _ in hits if c == "negation_not_but"]
        final = []
        for h in hits:
            if h[0] == "softening_adverb" and any(h[1] < y and x < h[2] for x, y in contra):
                continue
            if h[0] == "negation_comma_not" and any(h[1] < y and x < h[2] for x, y in notbut):
                continue
            final.append(h)
        for cat, a, b, msg in self.dedupe(final):
            self.emit(cat, a, b, msg)

    def rule_decimal(self, text: str, base: int, hits: list) -> None:
        v = self.view_obj
        for m in DECIMAL_RE.finditer(text):
            pos = base + m.start()
            if self.in_spans(pos, v.number_spans):
                continue
            before = text[max(0, m.start() - 20):m.start()]
            tok = re.search(r"(\S+)\s*$", before)
            if tok and tok.group(1).lower().rstrip("~") in self.exempt:
                continue
            hits.append(("decimal_in_prose", pos, base + m.end(), ""))

    def sentence_rules(self, sent: str, base: int, hits: list) -> None:
        for rx in NOT_BUT_PATTERNS:
            for m in rx.finditer(sent):
                hits.append(("negation_not_but", base + m.start(), base + m.end(), ""))
        for m in re.finditer(r"\brather\s+than\b", sent, re.I):
            hits.append(("rather_than", base + m.start(), base + m.end(), ""))
        if self.rx_signif:
            for m in self.rx_signif.finditer(sent):
                hits.append(("significance_announcer", base + m.start(), base + m.end(), ""))
        if self.rx_signif_init:
            m = self.rx_signif_init.match(sent)
            if m:
                hits.append(("significance_announcer", base + m.start(1), base + m.end(1), ""))
        for m in self.rx_comma_not.finditer(sent):
            hits.append(("negation_comma_not", base + m.start(), base + m.end(), ""))
        for m in re.finditer(r"\bsignificantly\b", sent, re.I):
            hits.append(("significantly", base + m.start(), base + m.end(), ""))
        for rx in self.rx_road:
            for m in rx.finditer(sent):
                hits.append(("roadmap", base + m.start(), base + m.end(), ""))
        if self.rx_contra:
            for m in self.rx_contra.finditer(sent):
                hits.append(("contradictory_pair", base + m.start(), base + m.end(), ""))
        if self.rx_adverb:
            for m in self.rx_adverb.finditer(sent):
                if re.search(r"\brather\s+than\s+$", sent[max(0, m.start() - 30):m.start()], re.I):
                    continue
                hits.append(("softening_adverb", base + m.start(), base + m.end(), ""))
        m = CLEFT_WHAT_RE.match(sent)
        if m and not sent.rstrip().endswith("?"):
            hits.append(("cleft_what", base + m.start(1), base + m.end(1), ""))
        m = CLEFT_IT_RE.match(sent)
        if m:
            first = (m.group(2).split() or [""])[0].strip(",").lower()
            if first not in self.it_exclude:
                hits.append(("cleft_it_that", base + m.start(1), base + m.end(), ""))
        m = CLEFT_THERE_RE.match(sent)
        if m:
            hits.append(("cleft_there_which", base + m.start(1), base + m.end(), ""))

    def paragraph_rules(self, text: str, base: int, sents: list, hits: list) -> None:
        # negation cascade
        flags = [bool(NEG_RE.search(text[s:e])) for s, e in sents]
        i = 0
        while i < len(flags):
            if flags[i]:
                j = i
                while j < len(flags) and flags[j]:
                    j += 1
                if j - i >= self.casc_min:
                    s, e = sents[i]
                    hits.append(("negation_cascade", base + s, base + e,
                                 f"{j - i} consecutive sentences rule out alternatives"))
                i = j
            else:
                i += 1
        # short paragraph end
        in_list = any(a < base + len(text) and base < b for a, b in self.view_obj.list_spans)
        if sents and not in_list and not (self.short_skip_single and len(sents) < 2):
            s, e = sents[-1]
            last = text[s:e]
            if not last.rstrip().endswith(":") and count_words(last) <= self.short_words:
                hits.append(("short_paragraph_end", base + s, base + e,
                             f"final sentence has {count_words(last)} words"))

    # -- structure checks --------------------------------------------------
    def check_headings(self) -> None:
        for a, b in self.view_obj.headings:
            txt = " ".join(self.view[a:b].split())
            reasons = []
            if ":" in txt or "?" in txt:
                reasons.append("contains ':' or '?'")
            if re.search(r"[^,]+,\s*[^,]+?,?\s+and\s+\S+", txt):
                reasons.append("three-item list")
            if re.search(r"(?:,\s*|\s+)(?:in full|revisited|in detail)\s*\W*$", txt, re.I):
                reasons.append("narrating suffix")
            if reasons:
                self.emit("heading", a, b, "; ".join(reasons), text=txt)

    def check_captions(self) -> None:
        for a, b in self.view_obj.captions:
            text = self.view[a:b]
            ns = len(split_sentences(text))
            nw = count_words(text)
            reasons = []
            if ns > self.cap_sent:
                reasons.append(f"{ns} sentences (max {self.cap_sent})")
            if nw > self.cap_words:
                reasons.append(f"{nw} words (max {self.cap_words})")
            if reasons:
                self.emit("caption_length", a, b, "; ".join(reasons), text=" ".join(text.split()))

    def check_title(self) -> None:
        for a, b in self.view_obj.titles:
            txt = " ".join(self.view[a:b].split())
            if ":" in txt or "?" in txt:
                self.emit("title", a, b, "title contains ':' or '?'", text=txt)

    def check_precision(self) -> None:
        clean = self.clean
        lo, hi = self.view_obj.body_start, self.view_obj.body_end
        pspans: list[tuple[int, int]] = []
        for rx in (P_EQ_RE, P_WORD_RE):
            for m in rx.finditer(clean, lo, hi):
                n = m.group("n")
                if sig_figs(n) > self.p_sig:
                    a, b = m.start(), m.end()
                    if any(a < y and x < b for x, y in pspans):
                        continue
                    pspans.append((a, b))
                    self.emit("pvalue_precision", a, b,
                              f"{sig_figs(n)} significant figures (max {self.p_sig})")
        # Monte Carlo numbers, per sentence of the prose view
        if self.sev.get("mc_precision") == "OFF":
            return
        for seg in self.segments():
            if seg.kind == "table":
                continue
            text = self.view[seg.a:seg.b]
            for s, e in split_sentences(text):
                if not MC_RE.search(text[s:e]):
                    continue
                a0, b0 = seg.a + s, seg.a + e
                for m in MC_NUM_RE.finditer(clean, a0, b0):
                    if sig_figs(m.group(0)) > self.p_sig:
                        if any(m.start() < y and x < m.end() for x, y in pspans):
                            continue
                        self.emit("mc_precision", m.start(), m.end(),
                                  f"{sig_figs(m.group(0))} significant figures in a Monte Carlo sentence")


# ---------------------------------------------------------------------------
# Public API and reports
# ---------------------------------------------------------------------------


def lint_text(raw: str, mode: str, cfg: dict, filename: str = "<input>") -> list[Finding]:
    return Linter(raw, mode, cfg, filename).run()


def summarize(findings: list[Finding], cfg: dict) -> dict:
    counts = {c: {"HARD": 0, "WARN": 0, "total": 0}
              for c in CATEGORIES if cfg["severity"].get(c) != "OFF"}
    for f in findings:
        counts[f.category][f.severity] += 1
        counts[f.category]["total"] += 1
    hard = sum(1 for f in findings if f.severity == "HARD")
    warn = sum(1 for f in findings if f.severity == "WARN")
    return {"counts": counts, "totals": {"HARD": hard, "WARN": warn, "total": len(findings)}}


def build_json(path: str, mode: str, findings: list[Finding], cfg: dict) -> dict:
    s = summarize(findings, cfg)
    return {"file": path, "mode": mode, "totals": s["totals"], "counts": s["counts"],
            "findings": [asdict(f) for f in findings]}


def md_escape(t: str) -> str:
    return t.replace("|", "\\|").replace("\n", " ")


def build_markdown(path: str, mode: str, findings: list[Finding], cfg: dict) -> str:
    s = summarize(findings, cfg)
    lines = [f"# Prose lint report: {path}", "",
             f"Mode: {mode}. HARD: {s['totals']['HARD']}. WARN: {s['totals']['WARN']}. "
             f"Total: {s['totals']['total']}.", "",
             "## Counts by category", "",
             "| Category | HARD | WARN | Total |", "| --- | ---: | ---: | ---: |"]
    for cat, c in s["counts"].items():
        lines.append(f"| {cat} | {c['HARD']} | {c['WARN']} | {c['total']} |")
    lines += ["", "## Findings", ""]
    for cat in s["counts"]:
        fs = [f for f in findings if f.category == cat]
        if not fs:
            continue
        lines += [f"### {cat} ({len(fs)})", "",
                  "| Line:Col | Severity | Match | Source line |", "| --- | --- | --- | --- |"]
        for f in fs:
            m = md_escape(f.match) + (f" ({md_escape(f.message)})" if f.message else "")
            lines.append(f"| {f.line}:{f.col} | {f.severity} | {m} | {md_escape(f.source_line)} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Prose linter for academic manuscripts.")
    ap.add_argument("path")
    ap.add_argument("--mode", choices=["latex", "text", "auto"], default="auto")
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--md", dest="md_out")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    p = Path(args.path)
    if not p.is_file():
        print(f"prose_lint: not a file: {p}", file=sys.stderr)
        return 2
    try:
        cfg = load_config(Path(args.config))
    except (OSError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"prose_lint: cannot load config: {exc}", file=sys.stderr)
        return 2
    mode = args.mode
    if mode == "auto":
        mode = "latex" if p.suffix.lower() == ".tex" else "text"
    raw = p.read_text(encoding="utf-8", errors="replace")
    findings = lint_text(raw, mode, cfg, str(p))

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(build_json(str(p), mode, findings, cfg), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8")
    if args.md_out:
        Path(args.md_out).write_text(build_markdown(str(p), mode, findings, cfg), encoding="utf-8")
    s = summarize(findings, cfg)
    if not args.quiet:
        print(f"prose_lint: {p} (mode {mode})")
        for cat, c in s["counts"].items():
            if c["total"]:
                print(f"  {cat:24s} HARD {c['HARD']:4d}  WARN {c['WARN']:4d}")
        t = s["totals"]
        print(f"  TOTAL: HARD {t['HARD']}, WARN {t['WARN']}, all {t['total']}")
    return 1 if s["totals"]["HARD"] else 0


if __name__ == "__main__":
    sys.exit(main())
