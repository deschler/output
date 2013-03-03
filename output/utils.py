# -*- coding: utf-8 -*-

# Copyright (c) 2013 Dirk Eschler
# Copyright (c) 1998-2013 Gentoo Foundation <http://www.gentoo.org/>
# Distributed under the terms of the GNU General Public License v2

import errno
import os
import subprocess
import sys


def writemsg(mystr, fd=None):
    """
    Prints out warning and debug messages based on the noiselimit setting.
    """
    if fd is None:
        fd = sys.stderr
    # # avoid potential UnicodeEncodeError
    # if isinstance(fd, io.StringIO):
    #     mystr = _unicode_decode(mystr,
    #         encoding=_encodings['content'], errors='replace')
    # else:
    #     mystr = _unicode_encode(mystr,
    #         encoding=_encodings['stdio'], errors='backslashreplace')
    #     if sys.hexversion >= 0x3000000 and fd in (sys.stdout, sys.stderr):
    #         fd = fd.buffer
    fd.write(mystr)
    fd.flush()


def get_term_size(fd=None):
    """
    Get the number of lines and columns of the tty that is connected to
    fd.  Returns a tuple of (lines, columns) or (0, 0) if an error
    occurs. The curses module is used if available, otherwise the output of
    `stty size` is parsed. The lines and columns values are guaranteed to be
    greater than or equal to zero, since a negative COLUMNS variable is
    known to prevent some commands from working (see bug Gentoo bug #394091).
    """
    if fd is None:
        fd = sys.stdout
    if not hasattr(fd, 'isatty') or not fd.isatty():
        return 0, 0
    try:
        import curses
        try:
            curses.setupterm(term=os.environ.get('TERM', 'unknown'), fd=fd.fileno())
            return curses.tigetnum('lines'), curses.tigetnum('cols')
        except curses.error:
            pass
    except ImportError:
        pass

    try:
        proc = subprocess.Popen(["stty", "size"], stdout=subprocess.PIPE, stderr=fd)
    except EnvironmentError as e:
        if e.errno != errno.ENOENT:
            raise
        # stty command not found
        return 0, 0

    #out = _unicode_decode(proc.communicate()[0])
    out = proc.communicate()[0]
    if proc.wait() == os.EX_OK:
        out = out.split()
        if len(out) == 2:
            try:
                val = (int(out[0]), int(out[1]))
            except ValueError:
                pass
            else:
                if val[0] >= 0 and val[1] >= 0:
                    return val
    return 0, 0
