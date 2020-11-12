#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  classes.py
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

# stdlib
from abc import ABC, abstractmethod
from decimal import Decimal
from collections import OrderedDict

# 3rd party
from typing import List

from cawdrey import AlphaDict
from domdf_python_tools import doctools


class LRPBase(ABC):
	@abstractmethod
	def __init__(self, *args, **kwargs):
		pass
	
	def __str__(self):
		return self.__repr__()
	
	def __iter__(self):
		for key, value in self.__dict__().items():
			yield key, value
	
	def __getstate__(self):
		return self.__dict__()
	
	def __setstate__(self, state):
		self.__init__(**state)
	
	def __copy__(self):
		return self.__class__(**self.__dict__())
	
	def __deepcopy__(self, memodict={}):
		return self.__copy__()
	
	@abstractmethod
	def __dict__(self):
		return dict()
	
	@classmethod
	@abstractmethod
	def from_series(cls, series):
		pass
		

class Sample(LRPBase):
	def __init__(
			self, sample_name, sample_type, instrument_name, position,
			user, acq_method, da_method, irm_cal_status, filename, results=None,
			):
		"""
		
		:param sample_name:
		:type sample_name:
		:param sample_type:
		:type sample_type:
		:param instrument_name:
		:type instrument_name:
		:param position:
		:type position:
		:param user:
		:type user:
		:param acq_method:
		:type acq_method:
		:param da_method:
		:type da_method:
		:param irm_cal_status:
		:type irm_cal_status:
		:param filename:
		:type filename:
		:param results:
		:type results:
		"""
		
		super().__init__()
		
		self.sample_name = sample_name
		self.sample_type = sample_type
		self.instrument_name = instrument_name
		self.position = position
		self.user = user
		self.acq_method = acq_method
		self.da_method = da_method
		self.irm_cal_status = irm_cal_status
		self.filename = filename
		
		if results is None:
			self._results = {}
		elif isinstance(results, dict):
			self._results = {}
			
			for cpd_no, compound in results.items():
				if isinstance(compound, dict):
					self._results[cpd_no] = Result(**compound)
				else:
					self._results[cpd_no] = compound
		elif isinstance(results, list):
			self._results = {}
			
			for compound in results:
				if isinstance(compound, dict):
					tmp_result = Result(**compound)
					cpd_no = tmp_result.index
					self._results[cpd_no] = tmp_result
				else:
					self._results[compound.index] = compound
		else:
			raise TypeError(f"Unknown type for `results`: {type(results)}")
			
	def add_result(self, result):
		self._results[result.index] = result
	
	@property
	def results_list(self):
		"""
		Returns a list of results in the order in which they were identified
		(i.e. sorted by the Cpd value from the csv export)

		:return:
		:rtype:
		"""
		
		results_list = []
		
		for key in sorted(self._results.keys()):
			results_list.append(self._results[key])
		
		return results_list
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return (
					self.sample_name == other.sample_name
					and self.sample_type == other.sample_type
					and self.filename == other.filename
					and self.acq_method == other.acq_method
					)
	
	@classmethod
	def from_series(cls, series):
		sample_name = series["Sample Name"]
		sample_type = series["Sample Type"]
		filename = series["File"]
		instrument_name = series["Instrument Name"]
		position = series["Position"]
		user = series["User Name"]
		acq_method = series["Acq Method"]
		da_method = series["DA Method"]
		irm_cal_status = series["IRM Calibration status"]
		
		return cls(
				sample_name, sample_type, instrument_name, position, user,
				acq_method, da_method, irm_cal_status, filename,
				)
	
	def __repr__(self):
		return f"Sample({self.sample_name})"
	
	def __dict__(self):
		return AlphaDict(
				sample_name=self.sample_name,
				sample_type=self.sample_type,
				instrument_name=self.instrument_name,
				position=self.position,
				user=self.user,
				acq_method=self.acq_method,
				da_method=self.da_method,
				irm_cal_status=self.irm_cal_status,
				filename=self.filename,
				results=self.results_list
				)


class Result(LRPBase):
	def __init__(
			self, cas, name, hits, index=-1, formula='', score=0.0,
			abundance=0, height=0, area=0, diff_mDa=0.0, diff_ppm=0.0,
			rt=0.0, start=0.0, end=0.0, width=0.0, tgt_rt=0.0, rt_diff=0.0,
			mz=0.0, product_mz=0.0, base_peak=0.0,
			mass=0.0, average_mass=0.0, tgt_mass=0.0,
			mining_algorithm='',
			z_count=0, max_z=0, min_z=0,
			n_ions=0, polarity='', label='',
			flags='', flag_severity='', flag_severity_code=0,
			):
		
		super().__init__()
		
		# Possible also AL (ID Source) and AM (ID Techniques Applied)
		self._cas = cas
		self.name = str(name)
		self.hits = hits
		self.formula = str(formula)
		self.score = Decimal(score)
		self.abundance = int(abundance)
		self.height = int(height)
		self.area = int(area)
		self.diff_mDa = Decimal(diff_mDa)
		self.diff_ppm = Decimal(diff_ppm)
		self.rt = Decimal(rt)
		self.start = Decimal(start)
		self.end = Decimal(end)
		self.width = Decimal(width)
		self.tgt_rt = Decimal(tgt_rt)
		self.rt_diff = Decimal(rt_diff)
		self.mz = Decimal(mz)
		self.product_mz = Decimal(product_mz)
		self.base_peak = Decimal(base_peak)
		self.mass = Decimal(mass)
		self.average_mass = Decimal(average_mass)
		self.tgt_mass = Decimal(tgt_mass)
		self.mining_algorithm = str(mining_algorithm)
		self.z_count = int(z_count)
		self.max_z = int(max_z)
		self.min_z = int(min_z)
		self.n_ions = int(n_ions)
		self.polarity = str(polarity)
		self.label = str(label)
		self.flags = str(flags)
		self.flag_severity = str(flag_severity)
		self.flag_severity_code = int(flag_severity_code)
		self.index = index  # Tracks the number of the result in the sample
	
	# "Score (Tgt)",
	@classmethod
	def from_series(cls, series):
		cas = series["CAS"]
		name = series["Name"]
		index = series["Cpd"]
		hits = series["Hits"]
		formula = series["Formula"]
		score = series["Score"]
		abundance = series["Abund"]
		height = series["Height"]
		area = series["Area"]
		diff_mDa = series["Diff (Tgt, mDa)"]
		diff_ppm = series["Diff (Tgt, ppm)"]
		rt = series["RT"]
		start = series["Start"]
		end = series["End"]
		width = series["Width"]
		tgt_rt = series["RT (Tgt)"]
		rt_diff = series["RT Diff (Tgt)"]
		mz = series["m/z"]
		product_mz = series["m/z (prod.)"]
		base_peak = series["Base Peak"]
		mass = series["Mass"]
		average_mass = series["Avg Mass"]
		tgt_mass = series["Mass (Tgt)"]
		mining_algorithm = series["Mining Algorithm"]
		z_count = series["Z Count"]
		max_z = series["Max Z"]
		min_z = series["Min Z"]
		n_ions = series["Ions"]
		polarity = series["Polarity"]
		label = series["Label"]
		flags = series["Flags (Tgt)"]
		flag_severity = series["Flag Severity (Tgt)"]
		flag_severity_code = series["Flag Severity Code (Tgt)"]
		
		return cls(
				cas, name, hits, index, formula, score,
				abundance, height, area, diff_mDa, diff_ppm,
				rt, start, end, width, tgt_rt, rt_diff,
				mz, product_mz, base_peak,
				mass, average_mass, tgt_mass,
				mining_algorithm,
				z_count, max_z, min_z,
				n_ions, polarity, label,
				flags, flag_severity, flag_severity_code,
				)
	
	def __repr__(self):
		return f"Result({self.name}; {self.formula}; {self.rt}; {self.score})"
	
	def __dict__(self):
		return AlphaDict(
				cas=self._cas,
				name=self.name,
				hits=self.hits,
				formula=self.formula,
				score=self.score,
				abundance=self.abundance,
				height=self.height,
				area=self.area,
				diff_mDa=self.diff_mDa,
				diff_ppm=self.diff_ppm,
				rt=self.rt,
				start=self.start,
				end=self.end,
				width=self.width,
				tgt_rt=self.tgt_rt,
				rt_diff=self.rt_diff,
				mz=self.mz,
				product_mz=self.product_mz,
				base_peak=self.base_peak,
				mass=self.mass,
				average_mass=self.average_mass,
				tgt_mass=self.tgt_mass,
				mining_algorithm=self.mining_algorithm,
				z_count=self.z_count,
				max_z=self.max_z,
				min_z=self.min_z,
				n_ions=self.n_ions,
				polarity=self.polarity,
				label=self.label,
				flags=self.flags,
				flag_severity=self.flag_severity,
				flag_severity_code=self.flag_severity_code,
				index=self.index,
				)


class SampleList(List[Sample]):
	
	@doctools.append_docstring_from(Sample.__init__)
	def add_new_sample(self, *args, **kwargs):
		"""
		Add a new sample to the list and return the
		:class:`~classes.Sample` object representing it.

		"""
		
		tmp_sample = Sample(*args, **kwargs)
		return self.add_sample(tmp_sample)
	
	def add_sample(self, sample):
		"""
		Add a :class:`~classes.Sample` object to the list.

		:param sample:
		:type sample: :class:`~classes.Sample`

		:return:
		:rtype:
		"""
		
		if sample in self:
			return self[self.index(sample)]
		else:
			self.append(sample)
			return sample
	
	def find_sample(self, sample_name):
		if sample_name in self:
			return self[self.index(sample_name)]
		else:
			return None
	
	def add_sample_from_series(self, series):
		"""
		Create a new sample object from a :class:`pandas.series` and
		add it to the list. The newly created :class:`~classes.Sample`
		object is returned.

		:param series:
		:type series: :class:`pandas.series`

		:return:
		:rtype: :class:`~classes.Sample`
		"""
		
		tmp_sample = Sample.from_series(series)
		return self.add_sample(tmp_sample)
	
	def sort_samples(self, key, reverse=False):
		"""
		Sort the list of Samples
		
		:param key: The name of the property in the sample to sort by
		:type key: str
		:param reverse: Whether the list should be sorted in reverse order. Default False
		:type reverse:
		
		:return:
		:rtype:
		"""
		
		self.sort(key=lambda samp: getattr(samp, key), reverse=reverse)

	def reorder_samples(self, order_mapping, key="sample_name"):
		"""
		Reorder the list of Samples

		:param order_mapping: A mapping between sample names and their new position in the list.
			For example:

				.. code-block:: python

					order_mapping = {
						"Propellant 1ug +ve": 0,
						"Propellant 1mg +ve": 1,
						"Propellant 1ug -ve": 2,
						"Propellant 1mg -ve": 3,
						}

		:type order_mapping: dict
		:param key: The name of the property in the sample to sort by. Default ``sample_name``
		:type key: str

		:return:
		:rtype:
		"""

		self.sort(key=lambda s: order_mapping[getattr(s, key)], reverse=True)

	def rename_samples(self, rename_mapping, key="sample_name"):
		"""
		Rename the samples in the list

		:param rename_mapping: A mapping between current sample names and their new names.
		Use ``None`` or omit the sample from the dictionary entirely to leave the name unchanged.

			For example:

				.. code-block:: python

					rename_mapping = {
						"Propellant 1ug +ve": "Alliant Unique 1µg/L +ESI",
						"Propellant 1mg +ve": "Alliant Unique 1mg/L +ESI",
						"Propellant 1mg -ve": None,
						}

		:type rename_mapping: dict
		:param key: The name of the property in the sample to sort by. Default ``sample_name``
		:type key: str

		:return:
		:rtype:
		"""

		for sample in self:
			if getattr(sample, key) in rename_mapping and rename_mapping[getattr(sample, key)]:
				sample.sample_name = rename_mapping.pop(getattr(sample, key))

	def get_areas_and_scores(self, compound_name, include_none=False):
		"""
		Returns two dictionaries: one containing sample names and peak areas for the
		compound with the given name, the other containing sample names and scores.
		
		:param compound_name:
		:type compound_name: str
		:param include_none: Whether samples where the compound was not found
			should be included in the results. Default False
		:type include_none: bool, optional
		
		:return:
		:rtype:
		"""
		
		peak_areas = OrderedDict()
		scores = OrderedDict()
		
		for sample in self:
			for result in sample.results_list:
				if result.name == compound_name:
					peak_areas[sample.sample_name] = result.area
					scores[sample.sample_name] = result.score
					break
			else:
				if include_none:
					peak_areas[sample.sample_name] = None
					scores[sample.sample_name] = None
		
		return peak_areas, scores
	
	def get_peak_areas(self, compound_name, include_none=False):
		"""
		Returns a dictionary containing sample names and peak areas for the
		compound with the given name.

		:param compound_name:
		:type compound_name: str
		:param include_none: Whether samples where the compound was not found
			should be included in the results. Default False
		:type include_none: bool, optional

		:return:
		:rtype:
		"""
		
		return self.get_areas_and_scores(compound_name, include_none)[0]
	
	def get_areas_for_compounds(self, compound_names, include_none=False):
		"""
		Returns a dictionary containing sample names and peak areas for the
		compounds with the given names.

		:param compound_names:
		:type compound_names: list of str
		:param include_none: Whether samples where none of the specified compounds
			were found should be included in the results. Default False.
		:type include_none: bool, optional

		:return:
		:rtype: SamplesAreaDict
		"""
		
		all_areas, all_scores = self.get_areas_and_scores_for_compounds(compound_names, include_none)
		return all_areas

	def get_areas_and_scores_for_compounds(self, compound_names, include_none=False):
		"""
		Returns two dictionaries: one containing sample names and peak areas for the
		compounds with the given names, the other containing sample names and scores.

		:param compound_names:
		:type compound_names: list of str
		:param include_none: Whether samples where none of the specified compounds
			were found should be included in the results. Default False.
		:type include_none: bool, optional

		:return:
		:rtype:
		"""

		tmp_all_areas = SamplesAreaDict()
		tmp_all_scores = SamplesScoresDict()

		for name in compound_names:
			areas = self.get_peak_areas(name, True)
			scores = self.get_scores(name, True)

			for sample_name, area in areas.items():
				if sample_name not in tmp_all_areas:
					tmp_all_areas[sample_name] = dict()
					tmp_all_scores[sample_name] = dict()

				tmp_all_areas[sample_name][name] = area
				tmp_all_scores[sample_name][name] = scores[sample_name]

		if include_none:
			return tmp_all_areas, tmp_all_scores

		else:
			all_areas = SamplesAreaDict()
			all_scores = SamplesScoresDict()

			for sample_name, compound_areas in tmp_all_areas.items():
				if any(list(compound_areas.values())):
					all_areas[sample_name] = compound_areas
					all_scores[sample_name] = tmp_all_scores[sample_name]

			return all_areas, all_scores

	def get_compounds(self) -> List[str]:
		"""
		Returns a list containing the names of the compounds present in the samples in alphabetical order.
		"""

		compounds = set()

		for sample in self:
			for result in sample.results_list:
				compounds.add(result.name)

		return sorted(compounds)

	def get_scores(self, compound_name, include_none=False):
		"""
		Returns a dictionary containing sample names and scores for the
		compound with the given name.

		:param compound_name:
		:type compound_name: str
		:param include_none: Whether samples where the compound was not found
			should be included in the results. Default False
		:type include_none: bool, optional

		:return:
		:rtype:
		"""
		
		return self.get_areas_and_scores(compound_name, include_none)[1]

	def filter(self, sample_names, key="sample_name", exclude=False):
		"""
		Filter the list to only contain sample_names whose name is in ``sample_names``.
		
		:param sample_names: A list of sample names to include
		:type sample_names: list of str
		:param key: The name of the property in the sample to sort by. Default ``sample_name``
		:type key: str
		:param exclude: If ``True``, any sample whose name is in ``sample_names``
			will be excluded from the output, rather than included.
			Default ``False``.
		:type exclude: bool, optional
		
		:return:
		:rtype: :class:`SampleList`
		"""
		
		new_sample_list = SampleList()
		
		for sample in self:
			if exclude:
				if getattr(sample, key) in sample_names:
					continue
			else:
				if getattr(sample, key) not in sample_names:
					continue
			
			new_sample_list.append(sample)
		
		return new_sample_list
	
	@property
	def sample_names(self):
		return [sample.sample_name for sample in self]
		
		
class BaseSamplePropertyDict(OrderedDict):
	"""
	OrderedDict to store a single property of a set of samples.
	Keys are the sample names and the values are dictionaries mapping compound names to property values.
	"""

	@property
	def sample_names(self):
		return list(self.keys())
	
	@property
	def n_samples(self):
		return len(self.keys())
	
	@property
	def n_compounds(self):
		for val in self.values():
			return len(val)


class SamplesAreaDict(BaseSamplePropertyDict):

	def get_compound_areas(self, compound_name):
		"""
		Get the peak areas for the given compound in every sample

		:param compound_name:
		:type compound_name:

		:return:
		:rtype:
		"""

		areas = []

		for sample_name, compound_areas in self.items():
			for name, area in compound_areas.items():
				if compound_name == name:
					if area is None:
						areas.append(0)
					else:
						areas.append(area)

		return areas


class SamplesScoresDict(BaseSamplePropertyDict):

	def get_compound_scores(self, compound_name):
		"""
		Get the peak scores for the given compound in every sample

		:param compound_name:
		:type compound_name:

		:return:
		:rtype:
		"""

		scores = []

		for sample_name, compound_scores in self.items():
			for name, score in compound_scores.items():
				if compound_name == name:
					if score is None:
						scores.append(0)
					else:
						scores.append(score)

		return scores