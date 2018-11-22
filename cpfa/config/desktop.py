# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"module_name": "CPFA",
			"color": "green",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": "CPFA"
		},
		{
			"module_name": "Fleet",
			"color": "purple",
			"icon": "octicon octicon-globe",
			"type": "module",
			"label": "Fleet"
		}
	]
