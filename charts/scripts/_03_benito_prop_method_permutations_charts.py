#!/usr/bin/env python3
#
#  _03_benito_prop_method_permutations_charts.py
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
from typing import List

# 3rd party
import numpy
from charts_shared import all_samples, chdir, mass_calibration_ranges
from domplotlib import create_figure
from mathematical.data_frames import set_display_options

# this package
from lcms_results_processor.chart_tools import savefig
from lcms_results_processor.charts import (
		ChartItem,
		make_rt_dataframe,
		plot_areas,
		plot_retention_times,
		sort_n_filter_by_filename,
		tex_page,
		tex_page_landscape,
		update_all_labels_with_cal_range
		)
from lcms_results_processor.utils import _1mg_l, _1ug_l, _10mg_l, sup_1, sup_2, warn_if_all_filtered

chart_items = [
		ChartItem.from_conditions(
				filename="Propellant_1ug_191126-0003-r001.d",  # solution 1
				sort_order=10,
				concentration=_1ug_l,
				esi=None,
				vol=None,
				new_name="(a)"
				),

		# just nitrobenzene
		ChartItem.from_conditions(
				filename="Propellant 1ug (2)_191206-0002.d",  # solution 2
				sort_order=20,
				concentration=_1ug_l,
				esi=None,
				vol=None,
				new_name="(b)",
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_191126-0002-r001.d",  # solution 1
				sort_order=30,
				concentration=_1mg_l,
				esi=None,
				vol=None,
				new_name="(a)",
				),
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0003.d",  # solution 2
				sort_order=40,
				concentration=_1mg_l,
				esi=None,
				vol=None,
				new_name="(b)",
				),

		# just nitrobenzene
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0006.d",  # solution 2
				dgt=200,
				sort_order=50,
				concentration=_1mg_l,
				esi=None,
				vol=None,
				new_name="(b)",
				),
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0007.d",  # solution 2
				dgf=14,
				sort_order=60,
				concentration=_1mg_l,
				esi=None,
				vol=None,
				new_name="(b)",
				),

		# just nitrobenzene
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0008.d",  # solution 2
				neb=50,
				sort_order=70,
				concentration=_1mg_l,
				esi=None,
				vol=None,
				new_name="(b)",
				),

		# just nitrobenzene
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0009.d",  # solution 2
				sort_order=80,
				dgf=14,
				neb=35,
				concentration=_1mg_l,
				esi=None,
				vol=None,
				new_name="(b)",
				),
		ChartItem.from_conditions(
				filename="Propellant_10mg_191128-0004-r001.d",  # solution 1
				sort_order=90,
				concentration=_10mg_l,
				esi=None,
				vol=None,
				new_name=f'(a){sup_1}',
				),
		ChartItem.from_conditions(
				filename="Propellant 10mg (1)_191206-00011.d",  # solution 1
				sort_order=100,
				concentration=_10mg_l,
				esi=None,
				vol=None,
				new_name=f'(a){sup_2}',
				),
		ChartItem.from_conditions(
				filename="Propellant 10mg (2)_191206-0004.d",  # solution 2
				sort_order=110,
				concentration=_10mg_l,
				esi=None,
				vol=None,
				new_name="(b)",
				),
		ChartItem.from_conditions(
				filename="Propellant 10mg (2)_191206-00010.d",  # solution 2
				sort_order=120,
				dgf=14,
				neb=35,
				concentration=_10mg_l,
				esi=None,
				vol=None,
				new_name="(b)",
				),
		]


def make_charts():
	chdir()

	# Display options for numpy and pandas
	set_display_options()

	update_all_labels_with_cal_range(chart_items, mass_calibration_ranges, ["50", "1700"])

	# Filter samples, reorder and rename
	target_samples = sort_n_filter_by_filename(all_samples, chart_items)
	all_identified_compounds: List[str] = target_samples.get_compounds()

	# Remove nitrobenzene
	all_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(target_samples, ["Nitrobenzene"])

	# fig, ax = create_figure(tex_page_landscape, left=0.165, bottom=0.17)  # without units
	fig, ax = create_figure(tex_page_landscape, left=0.135, bottom=0.17, top=0.09)
	fig, ax = plot_areas(fig, ax, target_samples, all_identified_compounds, show_scores=True, legend_cols=4, mz_range=(50, 1700))  # , include_none=True)
	# fig.suptitle("Peak Areas and Scores for Alliant Unique Propellant", fontsize=14, y=0.985)
	ax.set_ylabel("Concentration and Conditions")

	savefig(fig, "charts/benito_method_perms_propellant.png", dpi=600)
	savefig(fig, "charts/benito_method_perms_propellant.svg")

	# plt.show()
	fig, ax = create_figure(tex_page, left=0.215, bottom=0.13, top=0.02)

	fig, ax = plot_retention_times(fig, ax, target_samples, target_samples.get_compounds(), legend_cols=3)
	ax.set_ylabel("Concentration and Conditions")

	rt_data = make_rt_dataframe(target_samples.get_compounds(), target_samples)
	for compound, data in rt_data.iteritems():
		print(compound)
		stdev = numpy.nanstd(data)
		mean = numpy.nanmean(data)
		print(mean)
		rsd = stdev / mean
		print(f"{rsd:.3%}")
		print()

	savefig(fig, "charts/benito_method_perms_propellant_rt.png", dpi=600)
	savefig(fig, "charts/benito_method_perms_propellant_rt.svg")

	# plt.show()


if __name__ == "__main__":
	make_charts()
