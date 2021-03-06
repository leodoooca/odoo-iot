from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class IotDeviceInput(models.Model):
    _name = 'iot.device.input'

    name = fields.Char(required=True)
    device_id = fields.Many2one('iot.device', required=True, readonly=True)
    call_model_id = fields.Many2one('ir.model')
    call_function = fields.Char(required=True)
    serial = fields.Char()
    passphrase = fields.Char()
    action_ids = fields.One2many(
        'iot.device.input.action', inverse_name='input_id', readonly=True,
    )
    action_count = fields.Integer(compute='_compute_action_count')

    @api.depends('action_ids')
    def _compute_action_count(self):
        for r in self:
            r.action_count = len(r.action_ids)

    def _call_device(self, value):
        self.ensure_one()
        obj = self
        if self.call_model_id:
            obj = self.env[self.call_model_id.model].with_context(
                iot_device_input_id=self.id,
                iot_device_name=self.device_id.name,
                iot_device_id=self.device_id.id,
            )
        return getattr(obj, self.call_function)(value)

    def parse_args(self, serial, passphrase):
        if not serial or not passphrase:
            raise ValidationError(_('Serial and passphrase are required'))
        return [('serial', '=', serial), ('passphrase', '=', passphrase)]

    @api.model
    def get_device(self, serial, passphrase):
        return self.search(self.parse_args(serial, passphrase), limit=1)

    @api.model
    def get_auth_device(self, serial):
        return self.search([('serial', '=', serial)], limit=1)

    @api.multi
    def call_device(self, value):
        if not self:
            return {'status': 'error', 'message': _('Device cannot be found')}
        else:
            res = self._call_device(value)
            res['status'] = 'ok'
        self.env['iot.device.input.action'].create(
            self._add_action_vals(value, res))
        return res

    def _add_action_vals(self, value, res):
        return {
            'input_id': self.id,
            'args': str(value),
            'res': str(res),
        }

    def test_input_device(self, value):
        return {'value': value}


class IoTDeviceAction(models.Model):
    _name = 'iot.device.input.action'

    input_id = fields.Many2one('iot.device.input')
    args = fields.Char()
    res = fields.Char()
