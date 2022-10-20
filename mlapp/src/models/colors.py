# -*- coding: utf-8 -*-
from qgis.PyQt.QtGui import QColor

def toCssColour(*args):
    """Get a css representation of this colour."""
    moniker = "rgb" if len(args) == 3 else "rgba"
    return f"{moniker}({', '.join(map(str, args))})"

def toQgisRendererColour(*args):
    """Get a qgis renderer colour representation of this colour."""
    return ', '.join(map(str, args))

def toHexColour(r, g, b):
    """Get the colour associated with this status."""
    return (f"#{r:X}{g:X}{b:X}")

def toQColor(*args):
    """Get the colour associated with this status."""
    return QColor(*args)