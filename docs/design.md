# Design

The first issue I faced was about few companies being very strict on the allowed CV format, hence asking for the [EuroPass](https://europass.cedefop.europa.eu/it/documents/curriculum-vitae/templates-instructions/templates/doc) one, for example.
On the other hand, I really enjoyed _my_ custom format and didn't want to just drop it.
And what if another company would have come asking for a CV formatted following another format?

All of this led me considering templating my documents: many `tex` files as many formats I wanted to support and a single _database_ file keeping the information used to fill the templates.

On the other hand, I wanted my CV to be internationalized, maintaining a different version of each different format for each language supported.

After a first round in which I did implement all the features on my own (look at [erro@be0c83e](https://github.com/streambinder/erro/tree/be0c83eed88b6fac16a1dced69b913cc2c72ea2a) if interested), I moved to a more solid structure.

## Templating

Different formats, or templates, are to be made and accessing same data based on a sort of identifiers.
Despite how simple this issue could look, it's definitely not, at least if you want to keep something to be somehow proud.

Looking for a nice way to replace my old and misfiring templating engine, I discovered [jinja](https://jinja.palletsprojects.com/).
This library allows you to define `block_start_string`, `variable_start_string` and many other nice things to make it able to detect where exactly in your template you want placeholders and identifiers to be replaced with actual content.

This scales really good for LaTeX documents, actually:

- Python renderer:

```python
latex = jinja2.Environment(
    block_start_string='\\jblock{',
    block_end_string='}',
    variable_start_string='\\jvar{',
    variable_end_string='}'
)

latex.get_template('template.tex')
    .render(author = 'streambinder')
    .dump('resume.tex')
```

- LaTeX template `template.tex`:

```latex
\begin{document}

    \jvar{author}'s CV.

    \jblock{for i in range(5)}
        \jblock{if i % 2 == 0}
            \textit{ \jvar{i} }
        \jblock{endif}
    \jblock{endfor}

\end{document}
```

- LaTeX rendered `resume.tex`:

```latex
\begin{document}

streambinder's CV.

\textit{ 0 }
\textit{ 2 }
\textit{ 4 }

\end{document}
```

Making the engine take the rendering parameters from a database file was pretty easy, too.
The same result above can be achieved the following way:

```python
with open('database.yaml', 'r') as database_fd:
    latex.get_template('template.tex')
        .stream(yaml.safe_load(database_fd))
        .dump('resume.tex')
```

With `database.yaml` like below:

```yaml
author: streambinder
```

## Internationalization

Once you have a perfectly working template engine with support for external data source, supporting internationalization is straightforward: introduce a different database file for each language.

- Python renderer:

```python
for lang in ['en', 'it']:
    with open('database_{}.yaml'.format(lang), 'r') as database_fd:
        latex.get_template('template.tex')
            .stream(yaml.safe_load(database_fd))
```

- YAML english database `database_en.yaml`:

```yaml
author: streambinder in english
```

- YAML italian database `database_it.yaml`:

```yaml
author: streambinder in italiano
```
