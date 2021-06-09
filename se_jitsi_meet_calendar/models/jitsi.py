from odoo import models, fields, api
from random import choice


def create_hash():
    size = 32
    values = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    p = ''
    p = p.join([choice(values) for i in range(size)])
    return p


class JistiMeet(models.Model):
    _inherit = "calendar.event"


    def _get_default_participant(self):
        result = []
        result.append(self.env.user.id)
        return [(6, 0, result)]


    hash = fields.Char('Hash')
    date_formated = fields.Char(
        string='Date Formated',
        required=False)

    date_delay = fields.Float('Duration', required=True, default=1.0)
    url = fields.Char(string='URL to Meeting', compute='_compute_url')
    url_to_link = fields.Char(string='URL to link', compute='_compute_url')
    closed = fields.Boolean('Closed', default=False)
    current_user = fields.Many2one('res.users', compute='_get_current_user')
    domain = fields.Char( string='Domain',  required=False,compute='_compute_domain')
    is_password_required = fields.Boolean(
        string='Is username and password required?',
        required=False , default=False)
    password = fields.Char(
        string='Password',
        required=False)
    user = fields.Char(
        string='User',
        required=False)
    is_jitsi_meet = fields.Boolean(
    string='Is Jitsi Meet',
    required=False)

    def _compute_domain(self):
        for r in self:
            r.domain= self.env['ir.config_parameter'].sudo().get_param(
            'jitsi_calendar.meet_url',
            default='meet.jit.si')

    def _get_current_user(self):
        for rec in self:
            rec.current_user = self.env.user

    @api.model
    def create(self, vals):
        vals['hash'] = create_hash()
        res = super(JistiMeet, self).create(vals)
        return res

    def action_close_meeting(self):
        self.write({'closed': True})

    def action_reopen_meeting(self):
        self.write({'closed': False})

    def open(self):
       url=self.env['ir.config_parameter'].sudo().get_param('web.base.url',
           default='http://localhost:8011')
       return {'name': 'JITSI MEET',
               'res_model': 'ir.actions.act_url',
               'type': 'ir.actions.act_url',
               'target': 'new',
               'url': url+"/meet_calendar/"+str(self.id)
               }


    def _compute_url(self):
        config_url = self.env['ir.config_parameter'].sudo().get_param(
            'jitsi_calendar.meet_url',
            default='https://meet.jit.si/')
        url_site = self.env['ir.config_parameter'].sudo().get_param('web.base.url',
                                                               default='http://localhost:8011')
        if not self.hash:
            self.hash= create_hash()
        for r in self:
            if r.hash and r.name:
                r.url = config_url +r.hash
                r.url_to_link=url_site+"/meet_calendar/"+str(r.id)



    def send_mail(self):
        for record in self.partner_ids:
            template = self.env.ref('se_jitsi_meet_calendar.email_template_edi_se_jitsi_meet')
            _MAIL_TEMPLATE_FIELDS = ['subject', 'body_html', 'email_from', 'email_to',
                             'email_cc', 'reply_to', 'scheduled_date', 'attachment_ids']
            if template:
                 values = template.generate_email(self.id, _MAIL_TEMPLATE_FIELDS)

                 mail_mail_obj = self.env['mail.mail']
                 msg_id = mail_mail_obj.sudo().create(values)
                 if msg_id:
                     mail_mail_obj.sudo().send(msg_id)
                     mail_mail_obj.sudo().process_email_queue()


    def _format_date(self):
        for part in self:
            part.date_formated = fields.Datetime.from_string(part.start_datetime).strftime('%m/%d/%Y, %H:%M:%S')



