#!/usr/bin/env python3
#
#  chart_tools.py
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

# stdlib
import itertools
from typing import Iterable, Optional, Tuple

# 3rd party
import matplotlib
from domdf_python_tools.compat import importlib_resources
from domdf_python_tools.iterative import chunks
from domdf_python_tools.pagesizes import PageSize
from matplotlib import pyplot
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend import Legend

# this package
import lcms_results_processor

matplotlib.use("TkAgg")

# 3rd party
import matplotlib.pyplot

__all__ = ["savefig", "horizontal_legend", "create_figure", "plt"]

plt = matplotlib.pyplot

# print(plt.style.available)

# Good combinations

# >> White border, grey background, subdued colours
# plt.style.use('ggplot')

# >> White border, blue-grey background, nice coloured bars.
# >> Could have black border but might manage without
# plt.style.use('seaborn')

# plt.style.use('seaborn')
# plt.xkcd()

# >> FT paper border, grey background, nice coloured bars,
# >> but needs black border around figure and possibly black text
# plt.style.use('Solarize_Light2')

# plt.style.use('Solarize_Light2')
# plt.xkcd()

# >> Fixed version of above
with importlib_resources.path(lcms_results_processor, "domdf.mplstyle") as mystyle:
	plt.style.use(str(mystyle))

# >> White background, grey border, greyscale bars
# plt.style.use('grayscale')

# plt.style.use('grayscale')
# plt.xkcd()

# >> Pastel colours on black
# plt.style.use('dark_background')

# plt.style.use('default')

# plt.style.use('fivethirtyeight')
# plt.xkcd()


def savefig(fig, *args, **kwargs):
	if "facecolor" not in kwargs:
		kwargs["facecolor"] = fig.get_facecolor()

	if "edgecolor" not in kwargs:
		kwargs["edgecolor"] = None

	return fig.savefig(*args, **kwargs)


def horizontal_legend(
		fig: Figure,
		handles: Optional[Iterable[Artist]] = None,
		labels: Optional[Iterable[str]] = None,
		*,
		ncol: int = 1,
		**kwargs,
		) -> Legend:
	"""
	Place a legend on the figure, with the items arranged to read right to left rather than top to bottom.

	:param fig: The figure to plot the legend on.
	:param handles:
	:param labels:
	:param ncol: The number of columns in the legend.
	:param kwargs: Addition keyword arguments passed to :meth:`matplotlib.figure.Figure.legend`.
	"""

	if handles is None and labels is None:
		handles, labels = fig.axes[0].get_legend_handles_labels()

	# Rearrange legend items to read right to left rather than top to bottom.
	handles = list(filter(None, itertools.chain.from_iterable(itertools.zip_longest(*chunks(handles, ncol)))))
	labels = list(filter(None, itertools.chain.from_iterable(itertools.zip_longest(*chunks(labels, ncol)))))

	return fig.legend(handles, labels, ncol=ncol, **kwargs)


def create_figure(
		pagesize: PageSize,
		left: float = 0.2,
		bottom: float = 0.14,
		right: float = 0.025,
		top: float = 0.13,
		) -> Tuple[Figure, Axes]:
	"""
	Creates a figure with the given margins,
	and returns a tuple of the figure and its axes.

	:param pagesize:
	:param left: Left margin
	:param bottom: Bottom margin
	:param right: Right margin
	:param top: Top margin
	"""  # noqa: D400

	fig = pyplot.figure(figsize=pagesize)

	# [left, bottom, width, height]
	ax = fig.add_axes([left, bottom, 1 - left - right, 1 - top - bottom])

	return fig, ax
