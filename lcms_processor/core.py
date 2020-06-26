#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  core.py
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

# 3rd party
import pandas
import sdjson

# this package
from lcms_processor import Result, SampleList


def drop_columns(df, *, axis=1, inplace=True, **kwargs):
	# Columns where I have no idea what they represent
	unknown_cols = [
			"HMP", "KEGG", "LMP", "METLIN", "Notes", "Swiss-Prot",
			"CE", "Tgt Hit Pos", "Score Diff", "FV", "Saturated", "Vol",
			"Cpds/Group", "Group", "Std Dev", "Score (MFE)", "Vol %",
			"EIC/TIC% Area", "EIC/TIC% Height", "TIC% Area", "TIC% Height",
			"TWC% Area", "TWC% Height", "Purity Comments", "Purity Result",
			"Purity Value", "Score (Frag Coelution)", "FIs Conf.",
			"FIs Conf. %", "Score (Frag Ratio)", "FragMassDiff(ppm)",
			"FIs Eval.", "Source", "Flags",
			]
	
	db_cols = [
			"Mass (DB)", "Diff (DB, mDa)", "Diff (DB, ppm)",
			"RT (Lib/DB)", "RT Diff (Lib/DB)", "Score (DB)",
			"Shared (DB)", "Unique (DB)",
			]
	
	mfg_cols = [
			"Diff (MFG, mDa)", "Mass (MFG)", "Diff (MFG, ppm)", "Score (MFG)",
			]
	
	lib_cols = ["Lib/DB", "Score (Lib)"]
	
	new_df = df.drop([
			*unknown_cols,
			*db_cols,
			*mfg_cols,
			*lib_cols,
			],
			axis=axis, inplace=inplace, **kwargs)
	
	if inplace:
		return df
	else:
		return new_df


def reorder_columns(df):
	# Make sure to remove columns that got deleted earlier
	output_col_order = [
			"Sample Name", "Cpd", "CAS", "Name", "Hits", "Abund", "Mining Algorithm", "Area", "Base Peak", "Mass",
			"Avg Mass", "Score", "m/z", "m/z (prod.)", "RT", "Start", "End", "Width", "Diff (Tgt, mDa)",
			"Diff (Tgt, ppm)", "Score (Tgt)", "Flags (Tgt)", "Flag Severity (Tgt)", "Flag Severity Code (Tgt)",
			"Mass (Tgt)", "RT (Tgt)", "RT Diff (Tgt)", "Sample Type", "Formula", "Height", "Ions", "Polarity",
			"Z Count", "Max Z", "Min Z", "Label", "File", "Instrument Name", "Position", "User Name", "Acq Method",
			"DA Method", "IRM Calibration status", ]
	
	# Omitted columns
	# "ID Source", "ID Techniques Applied"
	# "MS/MS Count",		because blank
	
	return df[output_col_order]


def parse_masshunter_csv(csv_file, csv_outfile, json_outfile):
	# Read CSV file to data frame
	results_df = pandas.read_csv(csv_file, header=1, index_col=False, dtype=str)
	
	# drop unneeded columns
	drop_columns(results_df)
	
	rearranged_results_df = reorder_columns(results_df)
	rearranged_results_df.to_csv(csv_outfile, index=False)

	samples = SampleList()

	for row_idx, result in rearranged_results_df.iterrows():
		sample = samples.add_sample_from_series(result)
		tmp_result = Result.from_series(result)
		sample.add_result(tmp_result)

	with open(json_outfile, "w") as fp:
		sdjson.dump(samples, fp, indent=2)
