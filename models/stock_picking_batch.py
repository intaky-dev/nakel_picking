# -*- coding: utf-8 -*-

from odoo import models, fields, api
from collections import defaultdict


class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    def _get_consolidated_lines(self):
        """
        Consolidates move lines from all pickings in the batch.
        Groups by product, lot, package, source location and destination location.
        Returns a list of consolidated line dictionaries.
        """
        self.ensure_one()

        # Dictionary to accumulate quantities
        # Key: (product_id, lot_id, package_id, location_id, location_dest_id)
        consolidated = defaultdict(lambda: {
            'product': None,
            'product_name': '',
            'product_code': '',
            'lot': None,
            'lot_name': '',
            'package': None,
            'package_name': '',
            'result_package': None,
            'result_package_name': '',
            'location': None,
            'location_name': '',
            'location_dest': None,
            'location_dest_name': '',
            'quantity': 0.0,
            'uom': None,
            'uom_name': '',
            'picking_ids': [],
            'picking_names': [],
        })

        # Iterate through all pickings in the batch
        for picking in self.picking_ids:
            # Use move_line_ids for actual operations (with lot/package tracking)
            for move_line in picking.move_line_ids:
                # Skip lines without quantity
                if not move_line.quantity:
                    continue

                # Create the grouping key
                key = (
                    move_line.product_id.id,
                    move_line.lot_id.id if move_line.lot_id else False,
                    move_line.package_id.id if move_line.package_id else False,
                    move_line.location_id.id,
                    move_line.location_dest_id.id,
                )

                # Initialize or update the consolidated data
                if consolidated[key]['product'] is None:
                    consolidated[key].update({
                        'product': move_line.product_id,
                        'product_name': move_line.product_id.display_name,
                        'product_code': move_line.product_id.default_code or '',
                        'lot': move_line.lot_id,
                        'lot_name': move_line.lot_id.name if move_line.lot_id else '',
                        'package': move_line.package_id,
                        'package_name': move_line.package_id.name if move_line.package_id else '',
                        'result_package': move_line.result_package_id,
                        'result_package_name': move_line.result_package_id.name if move_line.result_package_id else '',
                        'location': move_line.location_id,
                        'location_name': move_line.location_id.display_name,
                        'location_dest': move_line.location_dest_id,
                        'location_dest_name': move_line.location_dest_id.display_name,
                        'uom': move_line.product_uom_id,
                        'uom_name': move_line.product_uom_id.name,
                    })

                # Accumulate quantity
                consolidated[key]['quantity'] += move_line.quantity

                # Track which pickings contributed to this line
                if picking.id not in consolidated[key]['picking_ids']:
                    consolidated[key]['picking_ids'].append(picking.id)
                    consolidated[key]['picking_names'].append(picking.name)

        # Convert to sorted list
        result = sorted(
            consolidated.values(),
            key=lambda x: (
                x['product_name'],
                x['lot_name'],
                x['location_name'],
                x['location_dest_name']
            )
        )

        return result

    def _get_consolidated_lines_by_product(self):
        """
        Alternative consolidation: only by product (no lot/package/location detail).
        This is useful for a simple summary view.
        """
        self.ensure_one()

        consolidated = defaultdict(lambda: {
            'product': None,
            'product_name': '',
            'product_code': '',
            'quantity': 0.0,
            'uom': None,
            'uom_name': '',
        })

        for picking in self.picking_ids:
            for move_line in picking.move_line_ids:
                if not move_line.quantity:
                    continue

                key = move_line.product_id.id

                if consolidated[key]['product'] is None:
                    consolidated[key].update({
                        'product': move_line.product_id,
                        'product_name': move_line.product_id.display_name,
                        'product_code': move_line.product_id.default_code or '',
                        'uom': move_line.product_uom_id,
                        'uom_name': move_line.product_uom_id.name,
                    })

                consolidated[key]['quantity'] += move_line.quantity

        result = sorted(
            consolidated.values(),
            key=lambda x: x['product_name']
        )

        return result
