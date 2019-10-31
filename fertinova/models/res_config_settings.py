import datetime
import logging
from pytz import timezone
import requests
from odoo import models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

BANXICO_DATE_FORMAT = '%d/%m/%Y'

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    # pylint: disable=W0702
    def _parse_banxico_data(self, available_currencies):
        """Parse function for Banxico provider.
        Overwrite the USD rate to use the fix value
        """
        icp = self.env['ir.config_parameter'].sudo()
        token = icp.get_param('banxico_token')
        if not token:
            # https://www.banxico.org.mx/SieAPIRest/service/v1/token
            token = 'd03cdee20272f1edc5009a79375f1d942d94acac8348a33245c866831019fef4'  # noqa
            icp.set_param('banxico_token', token)
        foreigns = {
            # position order of the rates from webservices
            'SF60653': 'USD',
        }
        url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/%s/datos/%s/%s?token=%s' # noqa
        try:
            date_mx = (
                datetime.datetime.now(timezone(
                    'America/Mexico_City')) + datetime.timedelta(days=1)
            ).strftime(DEFAULT_SERVER_DATE_FORMAT)
            res = requests.get(url % (
                ','.join(foreigns), date_mx, date_mx, token))
            res.raise_for_status()
            series = res.json()['bmx']['series']
            series = {serie['idSerie']: serie['datos'][0] for serie in series if 'datos' in serie}  # noqa
        except:  # noqa: E722
            return False

        available_currency_names = available_currencies.mapped('name')

        rslt = super(ResCompany, self)._parse_banxico_data(
            available_currencies)

        for index, currency in foreigns.items():
            if currency not in available_currency_names:
                continue
            if index not in series:
                _logger.info('Rate for currency %s not updated for date %s',
                             currency, date_mx)
                continue

            serie = series[index]
            try:
                foreign_mxn_rate = float(serie['dato'])
            except (ValueError, TypeError):
                _logger.info('Could not get rate for currency %s.', currency)
                continue
            foreign_rate_date = (datetime.datetime.strptime(serie.get(
                'fecha'), BANXICO_DATE_FORMAT) - datetime.timedelta(
                    days=1)).strftime(DEFAULT_SERVER_DATE_FORMAT)

            rslt[currency] = (1.0/foreign_mxn_rate, foreign_rate_date)
        return rslt
