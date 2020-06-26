#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  tgagg_pyplot.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import importlib_resources
import matplotlib

import lcms_processor

matplotlib.use("TkAgg")

import matplotlib.pyplot as plt

plt = plt

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
with importlib_resources.path(lcms_processor, "domdf.mplstyle") as mystyle:
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
