# Getting Started
All of this is still a work in progress and subject to change, so if you
want to follow and compile all the steps yourself, it's probably best to
just copy the setup I've prepared.

That is, it's not a requirement to use CentOS 7 or even a VM, most of
the interesting stuff happens inside a CentOS 6 Docker image.  But the
following is tested by me.

- Create a [CentOS 7](http://isoredirect.centos.org/centos/7/isos/x86_64/)
  VM.  I'm using KDE, but that (hopefully) shouldn't matter for these
  build instructions.

- Your login account's name will be used as the first part of the docker
  images, so pick a name accordingly (or modify the script).

- Use folders `~/dev<n>` where `<n>` is the step you want to build.
  It's assumed that everything happens in there if not explicitely
  stated otherwise.  Subsequent steps may have instructions to copy the
  necessary files from previous steps.  If you don't want to build a
  step yourself, make sure the files are in the right spot.

Now clone this repository somewhere and start with `step-0-basic-setup`.
Not everything in there will be applicable to your environment, but it
contains instructions for the developer tools, and in later steps you're
expected to have those installed.  Also, there's a script to set up the
files & folders in a reasonable manner.

Project organisation overview:

| Topic                        | build/ Subfolder                   | Target  |
|------------------------------|------------------------------------|---------|
| Setting it up locally        | step-0-basic-setup                 | &mdash; |
| manylinux2010 Docker images  | step-1-manylinux2010-docker-images | ~/dev1  |
| CentOS 6 RPM backports       | step-2-backports                   | ~/dev2  |
| Kivy almost-manylinux builds | step-3-kivy-almost-manylinux       | ~/dev3  |


### Tips:
- If you're going to experiment with docker containers, these can get
  big quite easily.  To be on the safe side, create a VM disk with a few
  tens of GB space (mine is 40 GB now).  Dynamic disk allocation works
  fine, but having to resize a disk/file system in CentOS 7 is a pain in
  the ass (speaking from experience).

- Give it enough RAM.  I've had trouble installing the live ISO with only
  1 GB RAM; 2 GB should be fine however.


# Optional: Emacs
Some script code is part of the various Emacs Org files which I use to
keep notes of everything.  It's not necessary to use Emacs at all, but
it might be easier to run things from within Emacs instead of
copy-pasting.  The code blocks `#+BEGIN_SRC ...` can be used directly.

If you're unfamiliar with Emacs, here's how to use it:

- key explanation:
  - `S-...` = Shift + ...
  - `C-...` = Ctrl + ...
  - `M-...` = Alt + ... (called *Meta* in Emacs)
- first, to add some generally useful defaults start Emacs.  Then do,
  including the parentheses:
  - `M-: (find-file user-init-file)`
  - now paste the following:
    ```elisp
    ;; Org Babel: load languages
    ;; may vary slightly with different versions of Org
    (org-babel-do-load-languages
     'org-babel-load-languages
     '((emacs-lisp . t)
       (python . t)
       (sh . t)))

    ;; backup creation config: among others, save in ~/.emacs.d/ subfolder
    ;; instead of clobbering the working directory
    (setq backup-directory-alist '(("." . "~/.emacs.d/backup"))
          backup-by-copying t
          version-control t
          kept-new-versions 20
          kept-old-versions 0
          delete-old-versions t
          vc-make-backup-files t)

    (defun backup-each-save ()
      (setq buffer-backed-up nil))

    (add-hook 'before-save-hook 'backup-each-save)

    ;; use UTF-8 by default
    (setq utf-translate-cjk-mode nil) ; disable CJK coding/encoding (Chinese/Japanese/Korean characters)
    (set-language-environment 'utf-8)
    (setq locale-coding-system 'utf-8)
    (set-default-coding-systems 'utf-8)
    (set-terminal-coding-system 'utf-8)
    (prefer-coding-system 'utf-8)

    ;; always show column number in status bar
    (column-number-mode)
    ```
- notable **Org Mode** key sequences:
  - `S-<tab>` 3 times to expand all sections
  - with the *point* (that's Emacs' name for the cursor) in a code block
    with `:tangle ...`
    - `C-u C-c C-v C-t` to create a script file (yes, in Emacs Org Mode
      that's called to *tangle* for some reason)
    - or `C-c C-v C-t` to create files for all code blocks in current
      buffer
  - in other code blocks:
    - `C-c C-c` to run it
    - `C-c '` to edit the source in a dedicated buffer for that language
- most important general key sequences:
  - pressed something wrong and want to get out: `C-g` (repeatedly if
    necessary)
  - open a file `C-x C-f` (called *find file* in Emacs)
  - scroll down/up: `C-v` `M-v`
  - end Emacs with `C-x C-c`
  - start selection: `C-<space>`
  - select a block: `M-h` (repeat to widen)
  - to easily modify a selection both ways you can `C-x C-x` to switch
        the *point* between start and end
  - copy: `M-w`
  - cut: `C-w`
  - paste: `C-y`
  - switch to other view: `C-x o` (in Emacs split views are called
    /windows/ and windows are called /frames/)
  - `C-h C-h` for a help overview
  - `C-h m` for mode description and keymaps
