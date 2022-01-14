# Pekin
Pekin is a simple templating engine for Python.

## Why Pekin?
Pekin is designed for simplicity, security, and compatibility.

Unlike other templating engines, Pekin barely uses regex, which means fewer errors. It has no package requirements.

Pekin is extremely lightweight. It only weighs 9 kilobytes.

## 🌟 Features
- Filters and parameters
- Escaping
- Loops
- Conditionals
- Executable Python
- HTML escaping
- Helpers (extensions)
- Partials
- Comments
- Easier template syntax
- Customizable template security

## 📦 Installation
You need to install Git CMD to download Pekin for Python.

Go to your Git CMD and type:
```shell
git clone "https://github.com/cardinal9999/Pekin"
cd Pekin
py
```


## 🎯 Basics
```
[!-- Comments start with '!--' and end with '--'. --]
[~Escaping brackets~]
[variables_example]
[!-- If statement --]
[if 2 + 2 == 4 | var]
[!-- Loop --]
[each *vars | it + 3]
Length: [length | var]
HTML Escape: [htmlescape | var]
```


## 👨‍💻 Using Pekin API

```py
import pekin
template = """
your template here
"""
a = pekin.Duck(template)
rendered = a.render(parameters = "add your variables here")
```

## 🦆 Help Improve Pekin!
Post an issue or pull request to help improve Pekin.
