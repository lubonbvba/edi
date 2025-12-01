# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import json,requests,re

import logging
logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    peppol_registered = fields.Boolean(help="Peppol registered")

    @api.multi
    def check_peppol(self):
        self.ensure_one()
        headers={}
        headers["X-API-KEY"] = (self.env['ir.config_parameter'].get_param('peppol_scrada_X-API-KEY'))
        headers["X-PASSWORD"] = (self.env['ir.config_parameter'].get_param('peppol_scrada_X-PASSWORD'))
        # headers["Content-Type"] = "application/xml"
        # headers["x-scrada-peppol-sender-scheme"] = "iso6523-actorid-upis"
        # headers["x-scrada-peppol-sender-id"] = "0208:" + self._ubl_get_company_id(self.company_id.partner_id.country_id.code,(self.company_id.partner_id.sanitized_vat))
        # headers["x-scrada-peppol-receiver-Scheme"] = "iso6523-actorid-upis"
        # headers["x-scrada-peppol-receiver-id"] = (self.env['ir.config_parameter'].get_param('peppol_overwrite_recipient')) or "0208:" +  self._ubl_get_company_id(self.partner_id.country_id.code,(self.partner_id.sanitized_vat))
        # headers["x-scrada-peppol-c1-country-code"] = self.company_id.partner_id.country_id.code
        # headers["x-scrada-peppol-document-type-scheme"] = "busdox-docid-qns"
        # headers["x-scrada-peppol-document-type-value"] = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2::Invoice##urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0::2.1"
        # headers["x-scrada-peppol-process-scheme"] = "cenbii-procid-ubl"
        # headers["x-scrada-peppol-process-value"] = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
        # headers["x-scrada-external-reference"] = self.number
        peppol_identifierScheme="iso6523-actorid-upis"
        peppol_IdentifierTypeBECBE="0208"
        pattern=r"^({})(\d+)$".format(re.escape(self.country_id.code))
        m = re.match(pattern, self.sanitized_vat, flags=re.IGNORECASE)
        vat_reg=m.group(2)
        url= self.env['ir.config_parameter'].get_param('peppol_base_url') + "/v1/company/" + self.env['ir.config_parameter'].get_param('peppol_scrada_company_id') + "/peppol/lookup/" + peppol_identifierScheme + "/" + peppol_IdentifierTypeBECBE + ":" + vat_reg
        logger.info("Scrada lookup url: %s", url)
        response = requests.get(url, headers=headers)
        if response.ok:
            self.peppol_registered=True
            logger.info("OK: Scrada response: %s", response.content)
        else: 
            logger.warning("Not OK: Scrada response: %s", response.content)


        logger.info("Scrada response: %s", response)

        # Optional: log response
#        logger.info("Scrada response status: %s", response.status_code)
