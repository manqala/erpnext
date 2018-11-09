
from frappe import _

def get_data():
	return [
		{
			"label": _("Workflow"),
			"icon": "fa fa-random",
			"items": [
				{
					"type": "doctype",
					"name": "Workflow Notifications",
					"description": _("Notifications for workflow actions.")
				},
			]
		},
	]
