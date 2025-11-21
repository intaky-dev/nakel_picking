# -*- coding: utf-8 -*-

from odoo import models, fields, api
from collections import defaultdict
import base64
import io


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

    def _generate_barcode_image(self, value, barcode_type='Code128', width=600, height=100):
        """
        Generate a barcode image as base64 string for embedding in PDF reports.

        :param value: The value to encode in the barcode
        :param barcode_type: Type of barcode (default: Code128)
        :param width: Width in pixels
        :param height: Height in pixels
        :return: base64 encoded image string with data URI prefix
        """
        if not value:
            return ''

        try:
            # Try using python-barcode library
            import barcode
            from barcode.writer import ImageWriter

            # Create barcode instance
            barcode_class = barcode.get_barcode_class(barcode_type.lower())
            barcode_instance = barcode_class(str(value), writer=ImageWriter())

            # Generate barcode to BytesIO buffer
            buffer = io.BytesIO()
            barcode_instance.write(buffer, options={
                'module_width': 0.3,
                'module_height': 10.0,
                'quiet_zone': 2.0,
                'font_size': 10,
                'text_distance': 3.0,
            })

            # Get image data and encode to base64
            buffer.seek(0)
            barcode_image = buffer.read()

            if barcode_image:
                # Convert to base64 with data URI
                return 'data:image/png;base64,' + base64.b64encode(barcode_image).decode('utf-8')

        except ImportError:
            # If python-barcode is not available, try reportlab
            try:
                from reportlab.graphics.barcode import code128
                from reportlab.lib.units import mm
                from reportlab.graphics import renderPM

                # Create barcode
                barcode_obj = code128.Code128(str(value), barHeight=15*mm, barWidth=0.8)

                # Render to image
                barcode_image = renderPM.drawToString(barcode_obj, fmt='PNG')

                if barcode_image:
                    return 'data:image/png;base64,' + base64.b64encode(barcode_image).decode('utf-8')

            except Exception as e:
                import logging
                _logger = logging.getLogger(__name__)
                _logger.warning(f'Error generating barcode with reportlab for value {value}: {str(e)}')

        except Exception as e:
            # Log the error but don't break the report
            import logging
            _logger = logging.getLogger(__name__)
            _logger.warning(f'Error generating barcode for value {value}: {str(e)}')

        return ''
