# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _
from odoo.addons.stock_location_tray.tests import common


class VerticalLiftCase(common.LocationTrayTypeCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.shuttle = cls.env.ref(
            'stock_vertical_lift.stock_vertical_lift_demo_shuttle_1'
        )
        cls.product_socks = cls.env.ref(
            'stock_vertical_lift.product_running_socks'
        )
        cls.product_recovery = cls.env.ref(
            'stock_vertical_lift.product_recovery_socks'
        )
        cls.vertical_lift_loc = cls.env.ref(
            'stock_vertical_lift.stock_location_vertical_lift'
        )

    @classmethod
    def _create_simple_picking_out(cls, product, quantity):
        stock_loc = cls.env.ref('stock.stock_location_stock')
        customer_loc = cls.env.ref('stock.stock_location_customers')
        picking_type = cls.env.ref('stock.picking_type_out')
        partner = cls.env.ref('base.res_partner_1')
        return cls.env['stock.picking'].create(
            {
                'picking_type_id': picking_type.id,
                'partner_id': partner.id,
                'location_id': stock_loc.id,
                'location_dest_id': customer_loc.id,
                'move_lines': [
                    (
                        0,
                        0,
                        {
                            'name': product.name,
                            'product_id': product.id,
                            'product_uom': product.uom_id.id,
                            'product_uom_qty': quantity,
                            'picking_type_id': picking_type.id,
                            'location_id': stock_loc.id,
                            'location_dest_id': customer_loc.id,
                        },
                    )
                ],
            }
        )

    @classmethod
    def _create_simple_picking_in(cls, product, quantity, dest_location):
        supplier_loc = cls.env.ref('stock.stock_location_suppliers')
        picking_type = cls.env.ref('stock.picking_type_in')
        partner = cls.env.ref('base.res_partner_1')
        return cls.env['stock.picking'].create(
            {
                'picking_type_id': picking_type.id,
                'partner_id': partner.id,
                'location_id': supplier_loc.id,
                'location_dest_id': dest_location.id,
                'move_lines': [
                    (
                        0,
                        0,
                        {
                            'name': product.name,
                            'product_id': product.id,
                            'product_uom': product.uom_id.id,
                            'product_uom_qty': quantity,
                            'picking_type_id': picking_type.id,
                            'location_id': supplier_loc.id,
                            'location_dest_id': dest_location.id,
                        },
                    )
                ],
            }
        )

    def _test_button_release(self, move_line):
        # for the test, we'll consider our last line has been delivered
        move_line.qty_done = move_line.product_qty
        move_line.move_id._action_done()
        # release, no further operation in queue
        operation = self.shuttle._operation_for_mode()
        result = operation.button_release()
        self.assertFalse(operation.current_move_line_id)
        self.assertEqual(operation.operation_descr, _("No operations"))
        expected_result = {
            "effect": {
                "fadeout": "slow",
                "message": _("Congrats, you cleared the queue!"),
                "img_url": "/web/static/src/img/smile.svg",
                "type": "rainbow_man",
            }
        }
        self.assertEqual(result, expected_result)
