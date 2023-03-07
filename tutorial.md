# Pekin Documentation
This is a guide to templating with Pekin. 🦆
## 1. Installing Pekin
You need to install git cmd to download Pekin for Python.

Go to your Git cmd and type:
```shell
git clone "https://github.com/cardinal9999/Pekin"
cd Pekin
py
```

Now, you can start using `import pekin` in the Python shell.

### Pekin in IDLE
You can still use Pekin in IDLE.

Put the `pekin` directory inside your Python project's directory to use Pekin.

## 2. Using Pekin API
This is the code for rendering a Pekin template:

```py
import pekin
template = """
Your template here
"""
duck = pekin.Duck(template)
rendered = duck.render(add=your, variables=here)
```

To create a Pekin template object, run `pekin.Duck(template_code)`. (You will soon learn the code for the making and rendering templates).

Note: rendering a template means running it. `duck.render(variables)` will return the text that the template has generated with `variables`.

### Toggling security

Pekin warns you if a template is trying to execute Python code.

This can be prevented by running this in the Python shell:

```py
duck.toggle_warning()
```

Only do this if you are 100% sure that the template isn't trying to execute malware.

---
## 3. Tags
Tags are code surrounded by square brackets `[]`.

The code is a mixture of other templating engines' tags like Underscore, Nunjucks, Jinja, Squirrelly, Mustache, and Handlebars.

Pekin does not use curly brackets because JavaScript has more curly brackets than square brackets.

Here is an example:
```py
from pekin import Duck
template = """
[!-- Hello world --]
Hello, [world]!
"""
d = Duck(template)
print(d.render(world="World"))
```

This will print:
`Hello, world!`

To put a variable in the template, we can insert the variable name in square brackets. This will render the variable's value.

The first line will be ignored because it is a comment tag.
Comments are documentation for the code. They are ignored by the parser.
They can be created by putting the comment text between `[!--` and `--]`

>🚩 Pekin is for security, so you can't evaluate Python expressions in tags. In most of the other templating engines, you can write `{{1 + 3}}` and it compile to `4`. This won't work in Pekin. If you want to evaluate Python expressions in templates, try creating an [extension](#8-extensions).

### Filters
Filters are like parameters in a Python function.

Filters come before the tag, and are separated by a vertical bar (`|`).

The vertical bar should have two spaces next to it.

#### Reverse
`[reverse | d]` -> `d = "lerriuqs"` -> `squirrel`

Reverses the string.

#### Length
`[length | d]` -> `d = "penguin"` -> `7`

Returns the length of an iterable.

#### Upper/Lower
`[upper | d] [lower | d]` -> `d = "Squirrel"` -> `squirrel SQUIRREL`

Changes the case the string is in.

### Parameters
Parameters are inputs for a tag or filter.

We can write parameters by putting an asterisk before the data.

Tags that use parameters:
#### Replace
`[replace *333 ==> 444 | a]` -> `a = "333444"` -> `444444`

The two parameters of the Python replace() function are separated by `" ==> "` with 2 spaces between it.

Note that the asterisk is ignored.

## 4. Escaping
Unlike other templating engines, Pekin ignores any text inside square brackets that isn't Pekin code. But what if our template was this web page you are reading right now?

The Pekin documentation is filled with Pekin code! But there is an easy way to escape all of the brackets.

### [~ Escaping Square Brackets ~]
To escape square brackets, we can replace the brackets with `[~` and `~]`.

And if we wanted to escape `[~ and ~]`, we can use `[!~~ and ~~!]`.

`[!~~ There is currently no way to escape this! ~~!]`


```
[!-- Escaping Example --]
[~Pekin~] [!-- Returns '[Pekin]' --]
[!~~Pekin~~!] [!-- Returns '[~Pekin~]' --]
```

### Escaping HTML
Pekin can escape HTML keywords in templates.

```
[htmlescape a]
```

Running it with `a = "<foo bar> <baz qux>"` will return `&lt;foo bar&gt; &lt;baz qux&gt;`

> Structure: [htmlescape key] = key: value to escape HTML

👾 You may have noticed the tag doesn't escape JavaScript quotes. Pekin is created for security, so it doesn't allow escaping strings of HTML, which can contain viruses.

## 5. Loops
### Looping text
One of Pekin's features are loops. Loops will execute some code for an iterator and output it. The iterator is any item inside an iterable.

Pekin has the `repeat` loop. Running `[*3 Key]` in Pekin is the same as `Key * 3` in Python.

> Structure: [*# Key] = Key: variable to repeat; #: Arbitrary number

Loops can be used to shorten the size of templates. However, they can also be used to create the XML entity lag bomb. Pekin restricts the number of text to repeat to 20.


Like other templating engines, Pekin supports for-loops.

For loops iterate through lists of data and do something with the iterator.

### For loops Pekin code
For loops are called `each loops` in Pekin.

```
[!-- For loops --]
[each *List | it + 3]
```

`it` is the iterator.

Running it with `List` being `[2, 5, 8, 3]` will return `58116`.
***
✔ Correct code: `[each *List | it + 3]`

❌ Incorrect code: `[each*List | it + 3]`

❌ Incorrect code: `[each *List|it + 3]`

IMPORTANT: **Pekin DOES NOT ignore whitespace!**
***
Because of a Pekin bug, you must put a new line between each `each` loop. This is also same with `if statements`.

> Structure: [each *KEY | CODE] = KEY: A list or iterable; CODE: code to execute

### Items Tag
Sometimes, each loops don't display data cleanly. Instead of writing each loops with code to display them cleanly, we can use the items tag to speed things up. The items tag returns all items of the iterable separated by space.

```
[!-- Items tag example --]
[items List]
```

Running it with `List` as `["Cat", "Dog", "Budgie"]` returns `Cat Dog Budgie`

We can add the newline filter: `[linefeed | items List]` prints:
```
Cat
Dog
Budgie
```

## 6. If Statements and Other Blocks
One of Pekin's features are conditionals.

In Python, there are if statements. If a Boolean/condition is true, some code will run.

### If Statement Pekin Code
```
[!-- If statements example --]
Hello, [if kwargs["a"] == "world!" | a]world!
```

✔ Correct code: ``[if 2 + 3 == 5 | a]``

❌ Incorrect code: ```[if 2 + 3 == 5|a]```

Running the code with `a` being equal to `world` will return:

```

Hello, world!
```

> Structure: [if code | key] = code: Python statement; key: variable to output if statement is true;

#### Restrictions
To prevent from executing malicious code, Pekin doesn't allow the strings `eval(` or `exec(` in conditions.

### Eval Tag
The `eval` tag is for evaluating Python code in variables.

`[eval a]` with `a = "2 + 2"` will return `4`.

> Structure [eval key] = key: the Python code to evaluate

## 7. Partials
Partials are like an entity in HTML. They allow you to reuse pieces of code in your template.

### Partials Pekin code
Python:

```python
p = """n
[each *a | it[0].replace("???", it[1]).replace("!?!", it[2])]""" # Define the partial
duck.toggle_warning()
duck.register_partial(p) # Set up the partial
```

Pekin:

```pekin
[$ n]
```

Input:

```py
a = ["<a href='???'>!?!</a>", "1.html", "Page 1"], ["<a href='???'>!?!</a>", "2.html", "Page 2"]
```

Output:

```html
<a href='1.html'>Page 1</a><a href='2.html'>Page 2</a>
```

You can register a partial by running `duck.register_partial("your partial")`. To use a partial, put the partial name after a dollar sign.

There are 2 lines in the partial's code: the first one is the **partial name**, and the second is the Pekin **code** for the partial.

## 8. Extensions
Partials can be used for reusing code, but it can't be used for creating your own Pekin code.

Extensions are the solution — they are like helpers in other templating engines.

### Extensions Pekin Code
We can use `duck.register_extension()` to add an extensions.

Python:
```python
ext = """[start code.pekin]
[duplicate | [==> it]]
[start code.py]
finish(kwargs[it] * 2)
"""
duck.register_extension(ext)
```

Pekin:
```
[duplicate | a]
```

Input: `a = "penguin "`

Output: `penguin penguin `

### Extension Structure
The code in the extension has 2 parts: `code.pekin` and `code.py`.

The `code.pekin` section contains the Pekin code that can be put in the template.

The `code.py` section contains the Python to execute for the Pekin parameter.


The parameter is the input for the extension. They are in the Pekin part of the extension as `[==> it]`. The input used in the template will be the variable `it` in the Python section.

> Note: because of a bug, **Pekin tags cannot have more than 1 parameter**.

#### The finish function
The finish function will replace the extension Pekin code in the template to the `val` variable. In the example, the tag will get the parameter and evaluate it.

### Extension Security
Extensions can be used to expand the limitations of Pekin. This is because extensions can do anything they want; Pekin doesn't scan them.

But this also means that malicious code can be executed in templates. Before registering any extension, review the extension's Python code and verify if it's safe. 
Don't use it if there is any sign of obfuscation.

### Extension for Evaluating Python
Extensions can almost do anything. This extension is going to evaluate Python code.

First create the extension:

```py
[start code.pekin]
[% [==> it] %]
[start code.py]
finish(eval(it))
```

Now, `register` the extension.

```py
import pekin
duck = pekin.Duck("any template here")
ext = """[start code.pekin]
[@ [==> it] @]
[start code.py]
finish(eval(it))"""
duck.register_extension(ext)
duck.render()
```

When you run this piece of code and change the template to yours, you can now evaluate Python expressions in the template.

Complex Python expressions like `2**7-3+1234^34**5-342*7//9+13&5`can be put into brackets `[@ @]` and render as `1358`.

> Tip: Access inputs in extensions: Pekin stores variable inputs in the dictionary `kwargs`. If you wanted to get a variable named `username`, then you can use `kwargs["username"]` in your extension.

Now get coding!
