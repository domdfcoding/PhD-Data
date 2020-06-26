#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  benito_prop_method_permutations_charts.py.py
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
from typing import List

from lcms_processor.charts import (
	A4_portrait,
	ChartItem,
	plot_areas,
	sort_n_filter_by_filename,
	update_all_labels_with_cal_range
)
from lcms_processor.tkagg_pyplot import plt, savefig  # isort: skip
from lcms_processor.utils import _1mg_l, _1ug_l, _10mg_l, set_display_options, sup_1, sup_2, warn_if_all_filtered

chart_items = [
		ChartItem.from_conditions(
				filename="Propellant_1ug_191126-0003-r001.d",  # solution 1
				sort_order=10,
				concentration=_1ug_l,
				esi=None, vol=None,
				new_name='(a)'
				),

		# just nitrobenzene
		ChartItem.from_conditions(
				filename="Propellant 1ug (2)_191206-0002.d",  # solution 2
				sort_order=20,
				concentration=_1ug_l,
				esi=None, vol=None,
				new_name='(b)',
				),
		ChartItem.from_conditions(
				filename="Propellant_1mg_191126-0002-r001.d",  # solution 1
				sort_order=30,
				concentration=_1mg_l,
				esi=None, vol=None,
				new_name='(a)',
				),
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0003.d",  # solution 2
				sort_order=40,
				concentration=_1mg_l,
				esi=None, vol=None,
				new_name='(b)',
				),

		# just nitrobenzene
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0006.d",  # solution 2
				dgt=200,
				sort_order=50,
				concentration=_1mg_l,
				esi=None, vol=None,
				new_name='(b)',
				),
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0007.d",  # solution 2
				dgf=14,
				sort_order=60,
				concentration=_1mg_l,
				esi=None, vol=None,
				new_name='(b)',
				),

		# just nitrobenzene
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0008.d",  # solution 2
				neb=50,
				sort_order=70,
				concentration=_1mg_l,
				esi=None, vol=None,
				new_name='(b)',
				),

		# just nitrobenzene
		ChartItem.from_conditions(
				filename="Propellant 1mg (2)_191206-0009.d",  # solution 2
				sort_order=80,
				dgf=14, neb=35,
				concentration=_1mg_l,
				esi=None, vol=None,
				new_name='(b)',
				),
		ChartItem.from_conditions(
				filename="Propellant_10mg_191128-0004-r001.d",  # solution 1
				sort_order=90,
				concentration=_10mg_l,
				esi=None, vol=None,
				new_name=f'(a){sup_1}',
				),
		ChartItem.from_conditions(
				filename="Propellant 10mg (1)_191206-00011.d",  # solution 1
				sort_order=100,
				concentration=_10mg_l,
				esi=None, vol=None,
				new_name=f'(a){sup_2}',
				),
		ChartItem.from_conditions(
				filename="Propellant 10mg (2)_191206-0004.d",  # solution 2
				sort_order=110,
				concentration=_10mg_l,
				esi=None, vol=None,
				new_name='(b)',
				),
		ChartItem.from_conditions(
				filename="Propellant 10mg (2)_191206-00010.d",  # solution 2
				sort_order=120,
				dgf=14, neb=35,
				concentration=_10mg_l,
				esi=None, vol=None,
				new_name='(b)',
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
	all_identified_compounds: List[str] = target_samples.get_compounds()

	# Remove nitrobenzene
	all_identified_compounds.remove("Nitrobenzene")
	warn_if_all_filtered(target_samples, ["Nitrobenzene"])

	fig, ax = plot_areas(target_samples, all_identified_compounds, show_scores=True)  # , include_none=True, legend_cols=3)
	fig.suptitle("Peak Areas and Scores for Alliant Unique Propellant", fontsize=14, y=0.985)

	# fig.set_size_inches(A4_portrait)
	fig.tight_layout()
	fig.subplots_adjust(bottom=0.13, top=0.91)

	savefig(fig, "charts/benito_method_perms_propellant.png", dpi=300)
	savefig(fig, "charts/benito_method_perms_propellant.svg")

	# plt.show()


if __name__ == '__main__':
	make_charts()
