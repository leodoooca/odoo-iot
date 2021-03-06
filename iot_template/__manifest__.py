# Copyright (C) 2018 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'IoT Templates',
    'version': '12.0.1.0.0',
    'category': 'IoT',
    'author': "Creu Blanca, "
              "Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'installable': True,
    'summary': 'IoT base module',
    'depends': [
        'iot_input',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/iot_device_input_usage_wizard.xml',
        'wizards/iot_device_apply_template.xml',
        'wizards/iot_device_configure.xml',
        'views/iot_device_views.xml',
        'views/iot_template_views.xml',
    ],
}
