# Copyright 2016 Jonathan Holloway <loadtheaccumulator@gmail.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/>.
#
"""All things ANSI color text output.

NOTE:
    Colorfiable is inherited by the Glusto class
    and not designed to be instantiated.
"""


class Colorfiable(object):
    """Defines and displays ANSI-compatible colors for string formatting."""
    # TODO: insert pep8/pylint ignore (python is all about readability, right?)

    # ANSI Background Bitwise Constants
    BG_DEFAULT =    1 << 0
    BG_BLACK =      1 << 1
    BG_RED =        1 << 2
    BG_GREEN =      1 << 3
    BG_YELLOW =     1 << 4
    BG_BLUE =       1 << 5
    BG_MAGENTA =    1 << 6
    BG_CYAN =       1 << 7
    BG_LTGRAY =     1 << 8
    BG_DKGRAY =     1 << 9
    BG_LTRED =      1 << 10
    BG_LTGREEN =    1 << 11
    BG_LTYELLOW =   1 << 12
    BG_LTBLUE =     1 << 13
    BG_LTMAGENTA =  1 << 14
    BG_LTCYAN =     1 << 15
    BG_WHITE =      1 << 16

    # ANSI Foreground Bitwise Constants
    DEFAULT =       1 << 17
    BLACK =         1 << 18
    RED =           1 << 19
    GREEN =         1 << 20
    YELLOW =        1 << 21
    BLUE =          1 << 22
    MAGENTA =       1 << 23
    CYAN =          1 << 24
    LTGRAY =        1 << 25
    DKGRAY =        1 << 26
    LTRED =         1 << 27
    LTGREEN =       1 << 28
    LTYELLOW =      1 << 29
    LTBLUE =        1 << 30
    LTMAGENTA =     1 << 31
    LTCYAN =        1 << 32
    WHITE =         1 << 33

    # ANSI Attribute Bitwise Constants
    NORMAL =        0
    BOLD =          1 << 34
    DIM =           1 << 35
    UNDERLINE =     1 << 36
    BLINK =         1 << 37
    REVERSE =       1 << 38
    HIDDEN =        1 << 39

    # Glusto Bitwise Aliases
    COLOR_COMMAND = BOLD | DKGRAY
    """Constant for command strings (BOLD | DKGRAY)"""
    COLOR_STDOUT =  BOLD | BG_LTGRAY | BLACK
    """Constant for stdout (BOLD | BG_LTGRAY | BLACK)"""
    COLOR_STDERR =  BOLD | RED
    """Constant for stderr (BOLD | RED)"""
    COLOR_RCODE =   BOLD | BLUE
    """Constant for command return code (BOLD | BLUE)"""

    _ANSI = {}

    # ANSI Attribute Values
    _ANSI[NORMAL] =         0
    _ANSI[BOLD] =           1
    # mileage varies on different terminals/apps
    _ANSI[DIM] =            2
    _ANSI[UNDERLINE] =      4
    _ANSI[BLINK] =          5
    _ANSI[REVERSE] =        7
    _ANSI[HIDDEN] =         8

    # ANSI Background Values
    _ANSI[BG_DEFAULT] =     49
    _ANSI[BG_BLACK] =       40
    _ANSI[BG_RED] =         41
    _ANSI[BG_GREEN] =       42
    _ANSI[BG_YELLOW] =      43
    _ANSI[BG_BLUE] =        44
    _ANSI[BG_MAGENTA] =     45
    _ANSI[BG_CYAN] =        46
    _ANSI[BG_LTGRAY] =      47
    _ANSI[BG_DKGRAY] =      100
    _ANSI[BG_LTRED] =       101
    _ANSI[BG_LTGREEN] =     102
    _ANSI[BG_LTYELLOW] =    103
    _ANSI[BG_LTBLUE] =      104
    _ANSI[BG_LTMAGENTA] =   105
    _ANSI[BG_LTCYAN] =      106
    _ANSI[BG_WHITE] =       107

    # ANSI Foreground Values
    _ANSI[DEFAULT] =        39
    _ANSI[BLACK] =          30
    _ANSI[RED] =            31
    _ANSI[GREEN] =          32
    _ANSI[YELLOW] =         33
    _ANSI[BLUE] =           34
    _ANSI[MAGENTA] =        35
    _ANSI[CYAN] =           36
    _ANSI[LTGRAY] =         37
    _ANSI[DKGRAY] =         90
    _ANSI[LTRED] =          91
    _ANSI[LTGREEN] =        92
    _ANSI[LTYELLOW] =       93
    _ANSI[LTBLUE] =         94
    _ANSI[LTMAGENTA] =      95
    _ANSI[LTCYAN] =         96
    _ANSI[WHITE] =          97

    @classmethod
    def colorfy(cls, color, message):
        """Applies ANSI terminal colors and attributes to strings.

        Args:
            color (int): Bitwise value(s) for color settings.
            message (str): String to wrap in the specified color.

        Returns:
            A color formatted string.

        Example:
            >>> g.colorfy(g.BG_CYAN | g.RED | g.BOLD, 'Bold red text on cyan')
        """
        log_color = cls.config.get('log_color', True)
        if not log_color:
            return message

        ansi_list = []
        for i in range(0, len(cls._ANSI) - 1):
            bitplace = 1 << i
            if color & bitplace:
                ansi_list.append(str(cls._ANSI[bitplace]))

        color_mod = ";".join(ansi_list)
        color_string = "\033[%sm{0}\033[0m" % color_mod
        try:
            color_message = "".join(color_string.format(message))
        except UnicodeEncodeError:
            encoded_message = message.encode(encoding='ascii',
                                             errors='replace')
            color_message = "".join(color_string.format(encoded_message))

        return color_message
