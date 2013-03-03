# -*- coding: utf-8 -*-

# Copyright (c) 2013 Dirk Eschler
# Copyright (c) 1998-2013 Gentoo Foundation <http://www.gentoo.org/>
# Distributed under the terms of the GNU General Public License v2

__docformat__ = 'epytext'

# Maps style class to tuple of attribute names
_styles = {}

# Maps attribute name to ansi code
codes = {}

esc_seq = '\x1b['

codes["normal"] = esc_seq + "0m"
codes["reset"] = esc_seq + "39;49;00m"

codes["bold"] = esc_seq + "01m"
codes["faint"] = esc_seq + "02m"
codes["standout"] = esc_seq + "03m"
codes["underline"] = esc_seq + "04m"
codes["blink"] = esc_seq + "05m"
codes["overline"] = esc_seq + "06m"
codes["reverse"] = esc_seq + "07m"
codes["invisible"] = esc_seq + "08m"

codes["no-attr"] = esc_seq + "22m"
codes["no-standout"] = esc_seq + "23m"
codes["no-underline"] = esc_seq + "24m"
codes["no-blink"] = esc_seq + "25m"
codes["no-overline"] = esc_seq + "26m"
codes["no-reverse"] = esc_seq + "27m"

codes["bg_black"] = esc_seq + "40m"
codes["bg_darkred"] = esc_seq + "41m"
codes["bg_darkgreen"] = esc_seq + "42m"
codes["bg_brown"] = esc_seq + "43m"
codes["bg_darkblue"] = esc_seq + "44m"
codes["bg_purple"] = esc_seq + "45m"
codes["bg_teal"] = esc_seq + "46m"
codes["bg_lightgray"] = esc_seq + "47m"
codes["bg_default"] = esc_seq + "49m"
codes["bg_darkyellow"] = codes["bg_brown"]

ansi_codes = []
for x in range(30, 38):
    ansi_codes.append('%im' % x)
    ansi_codes.append('%i;01m' % x)

rgb_ansi_colors = [
    '0x000000', '0x555555', '0xAA0000', '0xFF5555', '0x00AA00', '0x55FF55',
    '0xAA5500', '0xFFFF55', '0x0000AA', '0x5555FF', '0xAA00AA', '0xFF55FF',
    '0x00AAAA', '0x55FFFF', '0xAAAAAA', '0xFFFFFF'
]

for x in range(len(rgb_ansi_colors)):
    codes[rgb_ansi_colors[x]] = esc_seq + ansi_codes[x]

codes["black"] = codes["0x000000"]
codes["darkgray"] = codes["0x555555"]
codes["red"] = codes["0xFF5555"]
codes["darkred"] = codes["0xAA0000"]
codes["green"] = codes["0x55FF55"]
codes["darkgreen"] = codes["0x00AA00"]
codes["yellow"] = codes["0xFFFF55"]
codes["brown"] = codes["0xAA5500"]
codes["blue"] = codes["0x5555FF"]
codes["darkblue"] = codes["0x0000AA"]
codes["fuchsia"] = codes["0xFF55FF"]
codes["purple"] = codes["0xAA00AA"]
codes["turquoise"] = codes["0x55FFFF"]
codes["teal"] = codes["0x00AAAA"]
codes["white"] = codes["0xFFFFFF"]
codes["lightgray"] = codes["0xAAAAAA"]
codes["darkteal"] = codes["turquoise"]
# Some terminals have darkyellow instead of brown.
codes["0xAAAA00"] = codes["brown"]
codes["darkyellow"] = codes["0xAAAA00"]

# Colors from /etc/init.d/functions.sh
_styles["NORMAL"] = ("normal",)
_styles["GOOD"] = ("green",)
_styles["WARN"] = ("yellow",)
_styles["BAD"] = ("red",)
_styles["HILITE"] = ("teal",)
_styles["BRACKET"] = ("blue",)


def color(fg, bg="default", attr=None):
    if not attr:
        attr = ["normal"]
    mystr = codes[fg]
    for x in [bg] + attr:
        mystr += codes[x]
    return mystr


def style_to_ansi_code(style):
    """
    @param style: A style name
    @type style: String
    @rtype: String
    @return: A string containing one or more ansi escape codes that are
            used to render the given style.
    """
    ret = ""
    for attr_name in _styles[style]:
        # allow stuff that has found it's way through ansi_code_pattern
        ret += codes.get(attr_name, attr_name)
    return ret


def colorize(color_key, text):
    if color_key in codes:
        return codes[color_key] + text + codes["reset"]
    elif color_key in _styles:
        return style_to_ansi_code(color_key) + text + codes["reset"]
    else:
        return text


# compat_functions_colors = [
#     "bold", "white", "teal", "turquoise", "darkteal", "fuchsia", "purple",
#     "blue", "darkblue", "green", "darkgreen", "yellow", "brown", "darkyellow",
#     "red", "darkred"
# ]
#
#
# class CreateColorFunc(object):
#     __slots__ = ('_color_key',)
#
#     def __init__(self, color_key):
#         self._color_key = color_key
#
#     def __call__(self, text):
#         return colorize(self._color_key, text)
#
#
# for c in compat_functions_colors:
#     globals()[c] = CreateColorFunc(c)
