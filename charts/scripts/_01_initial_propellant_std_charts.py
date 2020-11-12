#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  initial_propellant_std_charts.py
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

# this package
from lcms_processor.charts import (
	ChartItem,
	create_figure, plot_areas,
	plot_retention_times, sort_n_filter_by_filename,
	tex_page, tex_page_landscape, update_all_labels_with_cal_range,
	)
from lcms_processor.utils import _1mg_l, _1ug_l, _2ul, set_display_options, warn_if_all_filtered

from lcms_processor.tkagg_pyplot import plt, savefig


# TODO injection volume: 1ug I think
chart_items = [
		ChartItem.from_conditions(
				filename="Propellant_1ug_+ve_191121-0003-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=10,
				vol=_2ul, esi=1,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_+ve_191121-0002-r001.d",
				new_name='',
				concentration=_1mg_l,
				sort_order=20,
				vol=_2ul, esi=1,
				),
		ChartItem.from_conditions(
				filename="Propellant_1ug_-ve_191121-0006-r001.d",
				new_name='',
				concentration=_1ug_l,
				sort_order=30,
				vol=_2ul, esi=-1,
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_-ve_191121-0005-r001.d",
				new_name='',
				concentration=_1mg_l,
				sort_order=40,
				vol=_2ul, esi=-1,
				),
		]


def make_charts():
	from charts_shared import all_samples, mass_calibration_ranges, chdir
	chdir()

	# Display options for numpy and pandas
	set_display_options()

	update_all_labels_with_cal_range(chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	target_samples = sort_n_filter_by_filename(all_samples, chart_items)
	all_identified_compounds = target_samples.get_compounds()

	# Remove nitrobenzene
	# all_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(target_samples, ["Nitrobenzene"])

	fig, ax = create_figure(tex_page_landscape, left=0.12)
	fig, ax = plot_areas(fig, ax, target_samples, all_identified_compounds, include_none=True, show_scores=True)
	fig.suptitle("Peak Areas and Scores for Alliant Unique Propellant", fontsize=14, y=0.985)
	# fig.subplots_adjust(bottom=0.11, top=0.90)

	savefig(fig, "charts/first_4_propellant_pos_and_neg.png", dpi=300)
	savefig(fig, "charts/first_4_propellant_pos_and_neg.svg")
	# plt.show()

	# worklist = load_json_worklist("data/worklist.json")
	# print(worklist)
	#
	# print(worklist.loc["Methanol Blank"])
	# print(worklist.loc[worklist["Sample Name"] == "Methanol Blank"])
	# print(worklist.loc[worklist["Sample Name"].str.startswith("Methanol")])

	fig, ax = create_figure(tex_page, left=0.15, bottom=0.17)

	fig, ax = plot_retention_times(fig, ax, target_samples, target_samples.get_compounds(), legend_cols=3)
	fig.suptitle("Retention Times for Alliant Unique Propellant", fontsize=14, y=0.985)
	ax.set_ylabel("Concentration and Conditions")

	plt.show()


if __name__ == '__main__':
	make_charts()