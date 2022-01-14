# Pekin
"""
Pekin - A templating engine with more features and security.
"""
import re
import html

__all__ = ["Duck"]

global foobar, iterableDataTypes, linefeed
foobar = chr(92)
iterableDataTypes = (str, list, set, frozenset)
linefeed = "\n"

def reEscape(inp):
    lst = "^[$].|(*)?+{,}"
    for l in lst:
        inp = inp.replace(l, foobar + l)
    return inp
def htmlEscape(val):
    return html.escape(val, 0)
def getQuotes(s):
    quote = []
    m = 0
    qt = ""
    for q in s:
        if q == '"' or  q == "'":
            if m == 0:
                m = 1
            else:
                m = 0
                quote.append(qt)
                qt = ""
        else:
            if m == 1:
                qt = qt + q
            else:
                pass
    return quote
class TemplateSecurityError(Exception):
    def __init__(self, msg):
        print("Template Security Error!!!")

class Duck(object):
    def __init__(self, template):
        self.template = template
        self.code_warn = 1
        self.partials = []
        self.tags = []
        self.finish = ""
    def toggle_warning(self):
        self.code_warn = (self.code_warn + 1) % 2

    def register_partial(self, partial):
        self.partials.append(partial.splitlines())
    def register_extension(self, tag):
        tag = tag.split("\n[start code.py]\n")
        tag[0] = tag[0].replace("[start code.pekin]\n", "")
        self.tags.append(tag)
    def render(self, **kwargs):
        string = self.template
        
        string = string.replace("[!--", chr(2))
        string = string.replace("--]", chr(26))
        nstring = string
        string = ""
        r = 0
        for random_thing in nstring:
            if random_thing == chr(2):
                r = 1
            elif random_thing == chr(26):
                r = 0
            else:
                if r != 1:
                    string = string + random_thing
        del nstring
        for tag in self.tags:
            found1 = re.findall(reEscape(tag[0]).replace('\\[==> it\\]', "(.*)"), string)[0]
            it = str(found1)
            def finish(e):
                self.finish = e
            exec(tag[1])
            string = string.replace(tag[0].replace('[==> it]', found1), self.finish)
            self.finish = ""
            
        for this, that in self.partials:
            string = string.replace("[$ " + this + "]", that)
            
        for key, value in kwargs.items():
            refound2= re.findall(f"{foobar}[replace {foobar}*(.*) {foobar}| {key}{foobar}]", string)
            refound1 = re.findall(f"{foobar}[each {foobar}*{key} {foobar}| (.*){foobar}]", string)
            refound = re.findall(f"{foobar}[if (.*) {foobar}| {key}{foobar}]", string)
            
            string = string.replace(f"[{key}]", str(value))
            
            for i in range(20):
                string = string.replace(f"[*{i} {key}]", str(value) * i)
            string = string.replace(f"[raw {key}]", f"[{key}]")

            if isinstance(value, str): string = string.replace(f"[items {key}]", " ".join(value))
            if isinstance(value, str):string = string.replace(f"[linefeed | items {key}]", "\n".join(value))
            
            string = string.replace(f"[length | {key}]", str(len(str(value))))
            string = string.replace(f"[reverse | {key}]", str(value)[::-1])

            string = string.replace(f"[upper | {key}]", str(value).upper())
            string = string.replace(f"[lower | {key}]", str(value).lower())

            if f"[eval {key}]" in string: string = string.replace(f"[eval {key}]", eval(value))
            for something in refound:
                if f"[if {something} | {key}]" in string:
                    something_1 = getQuotes(something)
                    something1 = something
                    for whatevs in something_1:
                        something1 = something1.replace("'" + whatevs + "'", "")
                        something1 = something1.replace('"' + whatevs + '"', "")
                    
                    
                    if self.code_warn == 0:
                        if eval(something): 
                            string = string.replace(f"[if {something} | {key}]", value)
                        else:
                            string = string.replace(f"[if {something} | {key}]", "")
                    else:
                        if "eval(" in something1 or "exec(" in something1: raise TemplateSecurityError("if statement cannot execute code as string")
                        a = input(f"""
[!] Warning from Pekin
-------------------------------
This template is trying to execute the following code:

{something}

Execute code? (y/n)
$ """)
                        if a == "y":
                            if eval(something): 
                                string = string.replace(f"[if {something} | {key}]", value)
                        else:
                          string = string.replace(f"[if {something} | {key}]", "")
            for something in refound1:
                if f"[each *{key} | {something}]" in string:
                    if not "it" in something:
                        raise TemplateSecurityError("code doesn't use iterator")
                    something_1 = getQuotes(something)
                    something1 = something
                    for whatevs in something_1:
                        something1 = something1.replace("'" + whatevs + "'", "")
                        something1 = something1.replace('"' + whatevs + '"', "")
                    if self.code_warn == 1:
                        if "eval(" in something1 or "exec(" in something1: raise TemplateSecurityError("each loop cannot execute code as string")
                        a = input(f"""
[!] Warning from Pekin
-------------------------------
This template is trying to execute the following code:

{something}

Execute code? (y/n)
$ """)
                        if a == "y":
                            e1 = ""
                            for it in value:
                                e1 = e1 + str(eval(something))
                            string = string.replace(f"[each *{key} | {something}]", e1)
                        else:
                            string = string.replace(f"[each *{key} | {something}]", '')
                    
                    else:
                        e1 = ""
                        for it in value:

                            e1 = e1 + str(eval(something))
                        string = string.replace(f"[each *{key} | {something}]", e1)
            for something in refound2:
                stVal = something
                something = something.replace(" ==> ", chr(4)
                                              )
                something = something.replace(" ---> ", " ==> ").split(chr(4))
                string = string.replace(f"[replace *{stVal} | {key}]", value.replace(something[0], something[1]))

            if f"[htmlescape {key}]" in string: string = string.replace(f"[htmlescape {key}]", htmlEscape(value))
        string = string.replace("[~", "[").replace("~]", "]").replace("[!~~", "[~").replace("~~!]", "~]")
        return string

def testPekin():
    template1 = """[!-- Testing Pekin --]==Pekin Test==

[raw Pekin]: [a]
Using eval: [eval b][c]
Using loops: [*4 d]
Using the items tag: [items e]
Using the linefeed filter: 
[linefeed | items e]
Length of a string: [length | f]
Using the reverse tag: [reverse | d]
Testing if: [raw if 4 == 6 | h] [if 'exec(' != "eval(" | h]
Upper and lower: [upper | h] [lower | h]
Each tag: [each *j | it + "\\n" ]
Replacing: [replace *????? ==> Pekin | i]
Testing escaping: [~Pekin Templating Engine~] [!~~Escaping~~!]
Test HTML: [htmlescape k]
Test partials: [$ abc]
Test extensions: [!penguin]
"""
    PekinExample1 = Duck(template1)
    PekinExample1.register_partial('abc\n[c]')
    ext = """[start code.pekin]
[!pengu[==> it]]
[start code.py]
print(it)
finish(it + 't')"""
    PekinExample1.register_extension(ext)
    print(PekinExample1.render(a="Duck.render(template)", b='"Pekin" + " "', c="Ducks", d="Quack! ", Pekin="Duck",
                               e=["Pekin Duck", "Mallard", "Northern Shoveler"], f="Pekin", g="key + ', ' + value",
                               h="Penguin", i="????? Duck", j =["print(6)", "3 - 4", "kwargs['f'] == 'Pekin' "],
                               k="<foo bar> <baz qux>"))

if __name__ == "__main__": testPekin()
