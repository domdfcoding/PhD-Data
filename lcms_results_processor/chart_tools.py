#!/usr/bin/env python3
#
#  chart_tools.py
"""

"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# 3rd party
from domdf_python_tools.typing import PathLike
from domplotlib import save_svg  # type: ignore[import]
from matplotlib.figure import Figure  # type: ignore[import]

__all__ = ["savefig"]


def savefig(fig: Figure, filename: PathLike, *args, **kwargs) -> None:
	r"""
	Save figure to a PNG, PDF, SVG etc.

	:param fig:
	:param filename: Output filename (with extension).
	:param \*args:
	:param \*\*kwargs:
	"""

	if "facecolor" not in kwargs:
		kwargs["facecolor"] = fig.get_facecolor()

	if "edgecolor" not in kwargs:
		kwargs["edgecolor"] = None

	filename = str(filename)
	if filename.endswith(".svg"):
		return save_svg(fig, filename, *args, **kwargs)
	else:
		return fig.savefig(filename, *args, **kwargs)
