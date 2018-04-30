"""
HTML5 contexts.

:author: Dominik Lang
:license: MIT
"""

import contextlib
import io
import sys


__all__ = ['create_document', 'tag', 'as_link']


class create_document(contextlib.redirect_stdout):
    """Redirect output to an HTML5 document specified by new_target.
    
    A HTML document title can be specified, but should not consist of
    whitespace only.  Default is a dash.
    
    For serialisation, an encoding is included and defaults to UTF-8.
    Make sure the output (likely ``new_target``) uses the correct one.
    
    Arguments are not checked for validity.
    """
    
    def __init__(self, new_target, *, title='-', encoding='utf-8'):
        super().__init__(new_target)
        self._title = str(title)
        self._encoding = encoding
    
    def __enter__(self):
        new_target = contextlib.redirect_stdout.__enter__(self)
        html5 = ('<!DOCTYPE html>\n'
                 '<html>\n'
                 '<title>{}</title>\n'
                 '<meta charset="{}">'.format(self._title, self._encoding))
        print(html5)
        return new_target


@contextlib.contextmanager
def tag(name):
    """Enclose output in an HTML tag denoted by the name."""
    print('<{}>'.format(name))
    yield
    print('</{}>'.format(name))


class LinkStringIO(io.StringIO):
    
    def __init__(self):
        super().__init__()
        self._write_text = False  # switch between link href="..." and text
    
    def write(self, s):
        if not s:
            return
        # else:
        if s.isspace():
            return super().write(s)
        # else:
        if self._write_text:
            count = super().write('<a href="')
            count += super().write(s)
            count += super().write('">')
        else:
            count = super().write(s)
            count += super().write('</a>')
        self._write_text = not self._write_text
        return count


class write_link(contextlib.redirect_stdout):
    """Combine any two subsequent non-empty writes into an HTML link."""
    
    def __init__(self):
        super().__init__(LinkStringIO())

    def __exit__(self, exctype, excinst, exctb):
        super().__exit__(exctype, excinst, exctb)
        with contextlib.closing(self._new_target):
            self._new_target.seek(0)
            sys.stdout.write(self._new_target.read())
