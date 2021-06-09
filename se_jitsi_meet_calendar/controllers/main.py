# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import logging

from odoo import http, tools, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class JistiMeet(http.Controller):
    @http.route('/meet_calendar/<int:id>/',type='http', auth="public", website=True)
    def jitsi_meet(self, id, **kwargs):
        record=request.env['calendar.event'].sudo().browse(id)
        if record:
            if not record.closed:
                data = {
                    'data': record,
                }
                return request.render("se_jitsi_meet_calendar.meet",data)
            else:
                return request.render("se_jitsi_meet_calendar.meet_closed")
        else:
            return request.render("se_jitsi_meet_calendar.meet_closed")