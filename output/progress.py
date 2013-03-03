# -*- coding: utf-8 -*-

# Copyright (c) 2013 Dirk Eschler
# Copyright (c) 1998-2013 Gentoo Foundation <http://www.gentoo.org/>
# Distributed under the terms of the GNU General Public License v2

import sys

from output.utils import get_term_size

__docformat__ = 'epytext'


class ProgressBar(object):
    """
    The interface is copied from the ProgressBar class from the EasyDialogs
    module (which is Mac only).
    """
    def __init__(self, title=None, maxval=0, label=None, max_desc_length=25):
        self._title = title or ''
        self._maxval = maxval
        self._label = label or ''
        self._curval = 0
        self._desc = ''
        self._desc_max_length = max_desc_length
        self._set_desc()

    @property
    def curval(self):
        """
        The current value (of type integer or long integer) of the progress
        bar. The normal access methods coerce curval between 0 and maxval. This
        attribute should not be altered directly.
        """
        return self._curval

    @property
    def maxval(self):
        """
        The maximum value (of type integer or long integer) of the progress
        bar; the progress bar (thermometer style) is full when curval equals
        maxval. If maxval is 0, the bar will be indeterminate (barber-pole).
        This attribute should not be altered directly.
        """
        return self._maxval

    def title(self, newstr):
        """
        Sets the text in the title bar of the progress dialog to newstr.
        """
        self._title = newstr
        self._set_desc()

    def label(self, newstr):
        """
        Sets the text in the progress box of the progress dialog to newstr.
        """
        self._label = newstr
        self._set_desc()

    def _set_desc(self):
        self._desc = "%s%s" % (
            "%s: " % self._title if self._title else "",
            "%s" % self._label if self._label else ""
        )
        if len(self._desc) > self._desc_max_length:  # truncate if too long
            self._desc = "%s..." % self._desc[:self._desc_max_length - 3]
        if len(self._desc):
            self._desc = self._desc.ljust(self._desc_max_length)

    def set(self, value, maxval=None):
        """
        Sets the progress bar's curval to value, and also maxval to max if the
        latter is provided. value is first coerced between 0 and maxval. The
        thermometer bar is updated to reflect the changes, including a change
        from indeterminate to determinate or vice versa.
        """
        if maxval is not None:
            self._maxval = maxval
        if value < 0:
            value = 0
        elif value > self._maxval:
            value = self._maxval
        self._curval = value

    def inc(self, n=1):
        """
        Increments the progress bar's curval by n, or by 1 if n is not
        provided. (Note that n may be negative, in which case the effect is a
        decrement.) The progress bar is updated to reflect the change. If the
        bar is indeterminate, this causes one ``spin'' of the barber pole. The
        resulting curval is coerced between 0 and maxval if incrementing causes
        it to fall outside this range.
        """
        self.set(self._curval + n)


class TermProgressBar(ProgressBar):
    """
    A tty progress bar similar to wget's.
    """
    def __init__(self, fd=sys.stdout, **kwargs):
        ProgressBar.__init__(self, **kwargs)
        lines, self.term_columns = get_term_size(fd)
        self.file = fd
        self._min_columns = 11
        self._max_columns = 80
        # For indeterminate mode, ranges from 0.0 to 1.0
        self._position = 0.0

    def set(self, value, maxval=None):
        ProgressBar.set(self, value, maxval=maxval)
        self._display_image(self._create_image())

    def _display_image(self, image):
        self.file.write('\r')
        self.file.write(image)
        self.file.flush()

    def _create_image(self):
        cols = self.term_columns
        if cols > self._max_columns:
            cols = self._max_columns
        min_columns = self._min_columns
        curval = self._curval
        maxval = self._maxval
        position = self._position
        percentage_str_width = 5
        square_brackets_width = 2
        if cols < percentage_str_width:
            return ""
        bar_space = cols - percentage_str_width - square_brackets_width - 1
        if self._desc:
            bar_space -= self._desc_max_length
        if maxval == 0:
            max_bar_width = bar_space - 3
            _percent = "".ljust(percentage_str_width)
            if cols < min_columns:
                return ""
            if position <= 0.5:
                offset = 2 * position
            else:
                offset = 2 * (1 - position)
            delta = 0.5 / max_bar_width
            position += delta
            if position >= 1.0:
                position = 0.0
            # Make sure it touches the ends
            if 1.0 - position < delta:
                position = 1.0
            if position < 0.5 and 0.5 - position < delta:
                position = 0.5
            self._position = position
            bar_width = int(offset * max_bar_width)
            image = '%s%s%s' % (
                self._desc, _percent, '[' + (bar_width * ' ') +
                    '<=>' + ((max_bar_width - bar_width) * ' ') + ']')
            return image
        else:
            percentage = int(100 * float(curval) / maxval)
            max_bar_width = bar_space - 1
            _percent = ('%d%% ' % percentage).rjust(percentage_str_width)
            image = '%s%s' % (self._desc, _percent)

            if cols < min_columns:
                return image
            offset = float(curval) / maxval
            bar_width = int(offset * max_bar_width)
            image = (
                image + '[' + (bar_width * '=') + '>' + ((max_bar_width - bar_width) * ' ') + ']')
            return image
