# -*- coding: utf-8 -*-

# Copyright (c) 2013 Dirk Eschler
# Copyright (c) 1998-2013 Gentoo Foundation <http://www.gentoo.org/>
# Distributed under the terms of the GNU General Public License v2

import sys
from output.colors import colorize

from output.utils import get_term_size, writemsg

__docformat__ = 'epytext'


class EOutput(object):
    """
    Performs fancy terminal formatting for status and informational messages.

    The provided methods produce identical terminal output to the eponymous
    functions in the shell script C{/sbin/functions.sh} and also accept
    identical parameters.

    This is not currently a drop-in replacement however, as the output-related
    functions in C{/sbin/functions.sh} are oriented for use mainly by system
    init scripts and ebuilds and their output can be customized via certain
    C{RC_*} environment variables (see C{/etc/conf.d/rc}). B{EOutput} is not
    customizable in this manner since it's intended for more general uses.
    Likewise, no logging is provided.

    @ivar quiet: Specifies if output should be silenced.
    @type quiet: BooleanType
    """
    def __init__(self, quiet=False):
        self.__last_e_cmd = ''
        self.__last_e_len = 0
        self.quiet = quiet
        lines, columns = get_term_size()
        if columns <= 0:
            columns = 80
        # Width of terminal in characters. Defaults to the value specified by
        # the shell's C{COLUMNS} variable, else to the queried tty size, else
        # to C{80}.
        self.term_columns = columns
        sys.stdout.flush()
        sys.stderr.flush()

    def _write(self, f, s):
        # Avoid potential UnicodeEncodeError
        writemsg(s, fd=f)

    def __eend(self, caller, errno, msg):
        if errno == 0:
            status_brackets = colorize(
                "BRACKET", "[ ") + colorize("GOOD", "ok") + colorize("BRACKET", " ]")
        else:
            status_brackets = colorize(
                "BRACKET", "[ ") + colorize("BAD", "!!") + colorize("BRACKET", " ]")
            if msg:
                if caller == "eend":
                    self.eerror(msg[0])
                elif caller == "ewend":
                    self.ewarn(msg[0])
        if self.__last_e_cmd != "ebegin":
            self.__last_e_len = 0
        if not self.quiet:
            out = sys.stdout
            self._write(
                out, "%*s%s\n" % (
                    (self.term_columns - self.__last_e_len - 7), "", status_brackets))

    def ebegin(self, msg):
        """
        Shows a message indicating the start of a process.

        @param msg: A very brief (shorter than one line) description of the starting process.
        @type msg: StringType
        """
        msg += " ..."
        if not self.quiet:
            self.einfon(msg)
        self.__last_e_len = len(msg) + 3
        self.__last_e_cmd = "ebegin"

    def eend(self, errno, *msg):
        """
        Indicates the completion of a process, optionally displaying a message
        via L{eerror} if the process's exit status isn't C{0}.

        @param errno: A standard UNIX C{errno} code returned by processes upon
                exit.
        @type errno: IntType
        @param msg: I{(optional)} An error message, typically a standard UNIX
                error string corresponding to C{errno}.
        @type msg: StringType
        """
        if not self.quiet:
            self.__eend("eend", errno, msg)
        self.__last_e_cmd = "eend"

    def eerror(self, msg):
        """
        Shows an error message.

        @param msg: A very brief (shorter than one line) error message.
        @type msg: StringType
        """
        out = sys.stderr
        if not self.quiet:
            if self.__last_e_cmd == "ebegin":
                self._write(out, "\n")
            self._write(out, colorize("BAD", " * ") + msg + "\n")
        self.__last_e_cmd = "eerror"

    def einfo(self, msg):
        """
        Shows an informative message terminated with a newline.

        @param msg: A very brief (shorter than one line) informative message.
        @type msg: StringType
        """
        out = sys.stdout
        if not self.quiet:
            if self.__last_e_cmd == "ebegin":
                self._write(out, "\n")
            self._write(out, colorize("GOOD", " * ") + msg + "\n")
        self.__last_e_cmd = "einfo"

    def einfon(self, msg):
        """
        Shows an informative message terminated without a newline.

        @param msg: A very brief (shorter than one line) informative message.
        @type msg: StringType
        """
        out = sys.stdout
        if not self.quiet:
            if self.__last_e_cmd == "ebegin":
                self._write(out, "\n")
            self._write(out, colorize("GOOD", " * ") + msg)
        self.__last_e_cmd = "einfon"

    def ewarn(self, msg):
        """
        Shows a warning message.

        @param msg: A very brief (shorter than one line) warning message.
        @type msg: StringType
        """
        out = sys.stderr
        if not self.quiet:
            if self.__last_e_cmd == "ebegin":
                self._write(out, "\n")
            self._write(out, colorize("WARN", " * ") + msg + "\n")
        self.__last_e_cmd = "ewarn"

    def ewend(self, errno, *msg):
        """
        Indicates the completion of a process, optionally displaying a message
        via L{ewarn} if the process's exit status isn't C{0}.

        @param errno: A standard UNIX C{errno} code returned by processes upon
                exit.
        @type errno: IntType
        @param msg: I{(optional)} A warning message, typically a standard UNIX
                error string corresponding to C{errno}.
        @type msg: StringType
        """
        if not self.quiet:
            self.__eend("ewend", errno, msg)
        self.__last_e_cmd = "ewend"
