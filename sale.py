#This file is part nereid_sale module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from nereid import render_template, request, login_required
from nereid.helpers import url_for
from nereid.contrib.pagination import Pagination
from werkzeug.exceptions import NotFound

from trytond.pool import PoolMeta

__all__ = ['Sale']
__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'

    per_page = 10

    @classmethod
    @login_required
    def render_list(cls):
        """
        Get sales
        """
        page = request.args.get('page', 1, int)

        clause = []
        clause.append(('party', '=', request.nereid_user.party))
        order = [('sale_date', 'DESC'), ('id', 'DESC')]

        sales = Pagination(
            cls, clause, page, cls.per_page, order
        )

        return render_template('sales.jinja', sales=sales)

    @classmethod
    @login_required
    def render(cls, uri):
        """
        Get sale detail
        """
        try:
            sale, = cls.search([
                ('id', '=', int(uri)),
                ('party', '=', request.nereid_user.party),
                ])
        except ValueError:
            return NotFound()
        return render_template('sale.jinja', sale=sale)

    def get_absolute_url(self, **kwargs):
        return url_for(
            'sale.sale.render', uri=self.id, **kwargs
            )
