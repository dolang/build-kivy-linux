#!/usr/bin/env python3.5
"""
pmpi — Poor Man's Package Index.


state: dev1, tested

Known shortcomings (besides the TODO below):

- generated HTML is not escaped (not too much of an issue allowed 
  characters in package names are limited)
- util.WheelNameInfo assumes there are no dashes in any of the parts,
  but that might not be true


TODO:

- https://www.python.org/dev/peps/pep-0503/
  "The URL SHOULD include a hash in the form of an URL fragment with the
  following syntax: #<hashname>=<hashvalue>, where <hashname> is the
  lowercase name of the hash function (such as sha256) and <hashvalue>
  is the hex encoded digest."

:author: Dominik Lang
:license: MIT
"""

from collections import defaultdict
import os
from pathlib import Path
import re

from redirect_html5 import (create_document, write_link as write_html_link,
                            tag as html_tag)
from util import parse_wheel_name


CWD = Path.cwd()


def assess(root_dir):
    """Inspect the working directory and make a *pmpi* blueprint."""
    blueprint = defaultdict(set)
    for wheel_path in root_dir.glob('*.whl'):
        wni = parse_wheel_name(wheel_path)  # a `WheelNameInfo`
        # gather all wheel files under the name of their respective
        # distribution:
        blueprint[wni.distribution].add(wheel_path.name)
    return blueprint


def _normalise_name(name):
    """Normalise the name according to PEP 503.
    
    See https://www.python.org/dev/peps/pep-0503/#normalized-names
    """
    return re.sub(r"[-_.]+", "-", name).lower()


def create(blueprint, root_dir):
    """Create the *pmpi* from a blueprint."""
    pmpi_dir = root_dir/'pmpi'
    pmpi_dir.mkdir(exist_ok=True)
    normalised_dist_names = [_normalise_name(dist_name) for dist_name in blueprint]
    pmpi_dist_dirs = [pmpi_dir/norm_name for norm_name in normalised_dist_names]
    
    # write root 'index.html' and create distribution directories
    with (pmpi_dir/'index.html').open('w', encoding='utf-8') as index, \
         create_document(index, title="pmpi — Poor Man's Package Index"):
        
        for norm_name, dist_dir in zip(normalised_dist_names, pmpi_dist_dirs):
            dist_dir.mkdir(exist_ok=True)
            with write_html_link():
                # write the normalised name as HTML link into the document
                # per the PEP the link itself must end with a '/'
                print((norm_name + '/'), norm_name, end='')
            print('<br>')
    
    # for each distribution create wheel symlinks and an 'index.html'
    pardir = Path(os.pardir)  # need it to be relative; usually, pardir is '..'
    for dist_name, dist_dir in zip(blueprint, pmpi_dist_dirs):
        with (dist_dir/'index.html').open('w', encoding='utf-8') as index, \
             create_document(index, title=dist_name):
            
            with html_tag('h1'):
                print(dist_name)
            for wheel_name in blueprint[dist_name]:
                wheel_symlink = dist_dir/wheel_name
                if wheel_symlink.exists():
                    wheel_symlink.unlink()
                wheel_symlink.symlink_to(pardir/pardir/wheel_name)
                with write_html_link():
                    print(wheel_name, wheel_name, end='')
                print('<br>')


def main():
    """Create the *pmpi* in the current working directory."""
    blueprint = assess(CWD)
    create(blueprint, CWD)


if __name__ == '__main__':
    main()
