from email import message
from openerp import fields
import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import json
import logging,pdb

_logger = logging.getLogger(__name__)
class ScradaBase(http.Controller):
    @http.route('/peppol/scrada', auth='public', type='json', methods=['POST'])
    def update(self, **kwargs):

        # _logger.info("SCRADA METHOD: %s", request.httprequest.method)
        # _logger.info("SCRADA HEADERS: %s", dict(request.httprequest.headers))
        # _logger.info("SCRADA QUERY PARAMS: %s", request.httprequest.args.to_dict())

        message = request.jsonrequest
#        _logger.info("SCRADA RAW BODY: %s", message)
        for k, v in message.items():
            _logger.info("%s = %s", k, v)
        if message["id"]:    
            invoice=request.env['account.invoice'].sudo().search([('peppol_ref','=',message["id"])])    
            if invoice:
                _logger.info ("Invoice found")
                invoice.sudo().peppol_state = message["status"]
                invoice.sudo().peppolC3MessageID = message["peppolC3MessageID"]
                invoice.sudo().peppol_state_time  = fields.datetime.now()

                invoice.sudo().peppol_error = message["errorMessage"]

            else:
                _logger.error ("Invoice found")


        # Return OK zodat Scrada niet opnieuw probeert
        return "OK"