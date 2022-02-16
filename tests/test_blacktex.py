import pytest

import blacktex


@pytest.mark.parametrize(
    "string, reference",
    [
        # dollar replacement:
        ("a $a + b = c$ b", r"a \(a + b = c\) b"),
        (r"a \$a + b = c\$ b", r"a \$a + b = c\$ b"),
        (r"a \\$a + b = c\\$ b", "a \\\\\n\\(a + b = c\\\\\n\\) b"),
        # text mods:
        (r"{\em it's me!}", r"\emph{it's me!}"),
        # comments:
        ("lorem  %some comment  \n %sit amet", "lorem "),
        ("% lorem some comment  \n sit amet", "sit amet"),
        ("A % lorem some comment  \n sit amet", "A sit amet"),
        ("{equation}%comment", "{equation}"),
        # multiple comment lines:
        ("A\n%\n%\nB", "A\nB"),
        # comment last:
        ("somemacro{%\nfoobar% \n}", "somemacro{foobar}"),
        # trailing whitespace:
        ("lorem    \n sit amet", "lorem\n sit amet"),
        # obsolete text mod:
        (r"lorem {\it ipsum dolor} sit amet", r"lorem \textit{ipsum dolor} sit amet"),
        # multiple spaces:
        ("lorem   ipsum dolor sit  amet", "lorem ipsum dolor sit amet"),
        # It's allowed as indentation at the beginning of lines:
        ("a\n    b\nc", "a\n    b\nc"),
        ("\\[\n  S(T)\\leq S(P_n).\n\\]\n", "\\[\n  S(T)\\leq S(P_n).\n\\]\n"),
        # spaces with brackets:
        (r"( 1+2 ) { 3+4 } \left( 5+6 \right)", r"(1+2) {3+4} \left(5+6\right)"),
        # multiple newlines:
        ("lorem  \n\n\n\n\n\n ipsum dolor   sit", "lorem\n\n\n ipsum dolor sit"),
        # $$:
        ("a $$a + b = c$$ b", "a\n\\[\na + b = c\n\\]\nb"),
        # whitespace after curly:
        ("\\textit{ \nlorem  \n\n\n ipsum   dol}", "\\textit{\nlorem\n\n\n ipsum dol}"),
        # sub/superscript space:
        ("2^ng", "2^n g"),
        ("1/n^3", "1/n^3"),
        ("n^3", "n^3"),
        ("(n^3)", "(n^3)"),
        ("n^\\alpha", "n^\\alpha"),
        ("a^2_PP^2", "a^2_PP^2"),
        # Underscore separation just produces too many false positives. Leave as is.
        ("2_ng", "2_ng"),
        # dots:
        ("a,...,b", "a,\\dots,b"),
        ("a,\\cdots,b", "a,\\dots,b"),
        # punctuation outside math:
        ("$a+b.$", "\\(a+b\\)."),
        (".$a+b$", ".\\(a+b\\)"),
        # <https://github.com/nschloe/blacktex/issues/43>
        (r"$a$\,$b$", r"\(a\)\,\(b\)"),
        # whitespace before punctuation:
        ("Some text .", "Some text."),
        # nbsp before ref:
        ("text \\ref{something}", "text~\\ref{something}"),
        # nbsp space:
        ("Some ~thing.", "Some thing."),
        # double nbsp:
        ("Some~~text.", "Some\\quad text."),
        # \over to \frac:
        ("a{b^{1+y} 2\\over 3^{4+x}}c", "a\\frac{b^{1+y} 2}{3^{4+x}}c"),
        ("{\\pi \\over4}", "\\frac{\\pi}{4}"),
        # overline warn:
        ("\\overline", "\\overline"),
        # linebreak after double backslash:
        ("T $2\\\\3 4\\\\\n6\\\\[2mm]7$.", "T \\(2\\\\\n3 4\\\\\n6\\\\\n[2mm]7\\)."),
        # keywords without backslash:
        (
            "maximum and logarithm $max_x log(x)$",
            r"maximum and logarithm \(\max_x \log(x)\)",
        ),
        # def vs. newcommand
        (r"\def\e{\text{r}}", r"\newcommand\e{\text{r}}"),
        # linebreak around begin/end:
        (
            "A\\begin{equation}a+b\\end{equation} B \n\\begin{a}\nd+e\n\\end{a}\nB",
            "A\n\\begin{equation}\na+b\n\\end{equation}\nB\n\\begin{a}\nd+e\n\\end{a}\nB",
        ),
        # indentation is okay
        (
            "A\n  \\begin{equation}\n  a+b\n  \\end{equation}",
            "A\n  \\begin{equation}\n  a+b\n  \\end{equation}",
        ),
        # centerline:
        ("\\centerline{foobar}", "{\\centering foobar}"),
        # eqnarray align:
        (
            "A\\begin{eqnarray*}a+b\\end{eqnarray*}F",
            "A\n\\begin{align*}\na+b\n\\end{align*}\nF",
        ),
        # env label:
        (
            "A\n\\begin{lemma}\n\\label{lvalpp}\\end{lemma}",
            "A\n\\begin{lemma}\\label{lvalpp}\n\\end{lemma}",
        ),
        ("A\n\\section{Intro}\n\\label{lvalpp}", "A\n\\section{Intro}\\label{lvalpp}"),
        (
            "A\n\\subsection{Intro}\n\\label{lvalpp}",
            "A\n\\subsection{Intro}\\label{lvalpp}",
        ),
        # coloneqq
        ("A:=b+c", "A\\coloneqq b+c"),
        ("A := b+c", "A \\coloneqq b+c"),
        ("A : = b+c", "A \\coloneqq b+c"),
        ("b+c =  : A", "b+c \\eqqcolon A"),
        # tabular column spec:
        (
            "\\begin{tabular} \n {ccc}\ncontent\\end{tabular}",
            "\\begin{tabular}{ccc}\ncontent\n\\end{tabular}",
        ),
        # env option spec:
        ("\\begin{table} \n [h!]G\\end{table}", "\\begin{table}[h!]\nG\n\\end{table}"),
        ("\\begin{table}   [h!]G\\end{table}", "\\begin{table}[h!]\nG\n\\end{table}"),
        ("\\begin{table}   [h!]\nG\\end{table}", "\\begin{table}[h!]\nG\n\\end{table}"),
        ("\\begin{table} \n [h!]G\\end{table}", "\\begin{table}[h!]\nG\n\\end{table}"),
        (
            "\\begin{table} \n [h!]\\label{foo}\\end{table}",
            "\\begin{table}[h!]\\label{foo}\n\\end{table}",
        ),
        (
            "\\begin{table} \n [h!]\\label{foo}\nG\\end{table}",
            "\\begin{table}[h!]\\label{foo}\nG\n\\end{table}",
        ),
        # space around operators:
        ("a+b=c", "a+b = c"),
        ("a+b&=&c", "a+b &=& c"),
        # SI percentage:
        (r"20\% \SI{30}{\%}", r"\SI{20}{\%} \SI{30}{\%}"),
        # escaped percentage sign:
        (r"25\% gain", r"\SI{25}{\%} gain"),
        # https://github.com/nschloe/blacktex/issues/46
        (r"\rightline{\bf a}", r"\rightline{\textbf{a}}"),
    ],
)
def test_compare(string, reference):
    print(repr(string))
    result = blacktex.clean(string)
    print(repr(result))
    print(repr(reference))
    assert result == reference


def test_readme():
    input_string = (
        "Because   of $$a+b=c$$ ({\\it Pythogoras}),\n"
        "% @johnny remember to insert name,\n"
        "and $y=2^ng$ with $n=1,...,10$, we have ${\\Gamma \\over 2}=8.$"
    )

    out = blacktex.clean(input_string)
    print(out)
    assert out == (
        "Because of\n"
        "\\[\n"
        "a+b = c\n"
        "\\]\n"
        "(\\textit{Pythogoras}),\n"
        "and \\(y = 2^n g\\) with \\(n = 1,\\dots,10\\), we have "
        "\\(\\frac{\\Gamma}{2} = 8\\)."
    )
