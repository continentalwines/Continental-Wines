# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class CwOrphanMove(models.Model):
    """
    Read-only SQL VIEW model: menampilkan stock.move yang bermasalah —
    yaitu moves yang terhubung ke SO (via picking.sale_id) tapi
    sale_line_id NULL atau to_refund FALSE padahal arah return
    (incoming dari customer location, state=done).

    Data di-generate dari SQL VIEW setiap query — tidak ada penyimpanan
    di tabel ini. Relasi ke stock.move dan sale.order.line tetap terjaga.
    """
    _name = 'cw.orphan.move'
    _description = 'Orphan Stock Move (Missing SO Line Link)'
    _auto = False
    _order = 'so_name, picking_name, move_id'

    # --- Relational fields ke record asli ---
    move_id = fields.Many2one('stock.move', string='Stock Move', readonly=True)
    picking_id = fields.Many2one('stock.picking', string='Transfer', readonly=True)
    so_id = fields.Many2one('sale.order', string='Sales Order', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    sale_line_id = fields.Many2one('sale.order.line', string='Current SOL', readonly=True)

    # --- Display fields ---
    picking_name = fields.Char(string='Transfer', readonly=True)
    picking_type_name = fields.Char(string='Op. Type', readonly=True)
    picking_origin = fields.Char(string='Source Doc', readonly=True)
    so_name = fields.Char(string='SO', readonly=True)
    product_code = fields.Char(string='Product Code', readonly=True)
    product_name = fields.Char(string='Product Name', readonly=True)
    move_qty = fields.Float(string='Qty', readonly=True)
    move_state = fields.Char(string='Move State', readonly=True)
    to_refund = fields.Boolean(string='To Refund', readonly=True)
    src_location = fields.Char(string='From Location', readonly=True)
    dst_location = fields.Char(string='To Location', readonly=True)
    src_usage = fields.Char(string='Src Usage', readonly=True)

    issue_type = fields.Selection([
        ('no_sale_line', 'sale_line_id NULL'),
        ('no_to_refund', 'to_refund FALSE'),
    ], string='Issue', readonly=True)

    # Suggested SOL: auto-computed, bisa dioverride user di form
    suggested_sol_id = fields.Many2one(
        'sale.order.line',
        string='Suggested SOL',
        compute='_compute_suggested_sol',
        readonly=True,
    )

    def init(self):
        """Create the SQL VIEW."""
        self.env.cr.execute("DROP VIEW IF EXISTS cw_orphan_move CASCADE")
        self.env.cr.execute("""
            CREATE VIEW cw_orphan_move AS
            SELECT
                sm.id                           AS id,
                sm.id                           AS move_id,
                sm.picking_id                   AS picking_id,
                sp.name                         AS picking_name,
                spt.name->>'en_US'              AS picking_type_name,
                sp.origin                       AS picking_origin,
                sp.sale_id                      AS so_id,
                so.name                         AS so_name,
                sm.product_id                   AS product_id,
                pp.default_code                 AS product_code,
                pt.name->>'en_US'               AS product_name,
                sm.quantity                     AS move_qty,
                sm.state                        AS move_state,
                COALESCE(sm.to_refund, FALSE)   AS to_refund,
                sm.sale_line_id                 AS sale_line_id,
                sl_src.complete_name            AS src_location,
                sl_dst.complete_name            AS dst_location,
                sl_src.usage                    AS src_usage,
                CASE
                    WHEN sm.sale_line_id IS NULL THEN 'no_sale_line'
                    ELSE 'no_to_refund'
                END                             AS issue_type
            FROM stock_move sm
            JOIN stock_picking sp           ON sp.id = sm.picking_id
            JOIN stock_picking_type spt     ON spt.id = sp.picking_type_id
            JOIN sale_order so              ON so.id = sp.sale_id
            JOIN product_product pp         ON pp.id = sm.product_id
            JOIN product_template pt        ON pt.id = pp.product_tmpl_id
            JOIN stock_location sl_src      ON sl_src.id = sm.location_id
            JOIN stock_location sl_dst      ON sl_dst.id = sm.location_dest_id
            WHERE
                sm.state = 'done'
                AND sm.scrapped = FALSE
                AND sp.sale_id IS NOT NULL
                AND sl_src.usage = 'customer'
                AND sl_dst.usage = 'internal'
                AND (
                    sm.sale_line_id IS NULL
                    OR (
                        sm.sale_line_id IS NOT NULL
                        AND COALESCE(sm.to_refund, FALSE) = FALSE
                    )
                )
        """)

    @api.depends('so_id', 'product_id', 'sale_line_id')
    def _compute_suggested_sol(self):
        for rec in self:
            if not rec.so_id or not rec.product_id:
                rec.suggested_sol_id = False
                continue
            # Auto-match: cari SOL di SO yang sama dengan product sama
            sol = self.env['sale.order.line'].search([
                ('order_id', '=', rec.so_id.id),
                ('product_id', '=', rec.product_id.id),
                ('display_type', '=', False),
            ], limit=1)
            if not sol:
                # Fallback: match via product template
                sol = self.env['sale.order.line'].search([
                    ('order_id', '=', rec.so_id.id),
                    ('product_id.product_tmpl_id', '=', rec.product_id.product_tmpl_id.id),
                    ('display_type', '=', False),
                ], limit=1)
            rec.suggested_sol_id = sol

    def _do_fix(self, sol_id_override=None):
        """
        Core fix logic: assign sale_line_id + set to_refund=True pada move,
        lalu trigger recompute qty_delivered pada SOL terkait.

        sol_id_override: dict {move_id: sol_id} jika user override manual.
        """
        if not self:
            return []

        fixed = []
        skipped = []

        for rec in self:
            move_id = rec.move_id.id
            so_id = rec.so_id.id

            # Prioritas: override manual → suggested → auto-match
            sol_id = None
            if sol_id_override and move_id in sol_id_override:
                sol_id = sol_id_override[move_id]
            elif rec.suggested_sol_id:
                sol_id = rec.suggested_sol_id.id

            # Fallback SQL jika compute tidak berhasil
            if not sol_id:
                self.env.cr.execute("""
                    SELECT sol.id
                    FROM sale_order_line sol
                    WHERE sol.order_id = %s
                      AND sol.product_id = %s
                      AND sol.display_type IS NULL
                    ORDER BY sol.id LIMIT 1
                """, [so_id, rec.product_id.id])
                row = self.env.cr.fetchone()
                if not row:
                    self.env.cr.execute("""
                        SELECT sol.id
                        FROM sale_order_line sol
                        JOIN product_product pp ON pp.id = sol.product_id
                        WHERE sol.order_id = %s
                          AND pp.product_tmpl_id = (
                              SELECT product_tmpl_id FROM product_product WHERE id = %s
                          )
                          AND sol.display_type IS NULL
                        ORDER BY sol.id LIMIT 1
                    """, [so_id, rec.product_id.id])
                    row = self.env.cr.fetchone()

                if row:
                    sol_id = row[0]

            if not sol_id:
                skipped.append(
                    "Move %s [%s] SO %s: tidak ada SOL matching."
                    % (move_id, rec.product_code or rec.product_name, rec.so_name)
                )
                continue

            self.env.cr.execute("""
                UPDATE stock_move
                SET sale_line_id = %s,
                    to_refund    = TRUE
                WHERE id = %s
            """, [sol_id, move_id])

            fixed.append(sol_id)

        return fixed, skipped

    def action_fix_one(self):
        """Fix satu record dari button per-row di list."""
        self.ensure_one()
        fixed, skipped = self._do_fix()

        if not fixed:
            raise UserError("Tidak bisa fix:\n" + "\n".join(skipped))

        # Recompute
        sol_records = self.env['sale.order.line'].browse(list(set(fixed)))
        sol_records.invalidate_recordset()
        sol_records._compute_qty_delivered()
        sol_records.modified(['qty_delivered'])
        self.env.flush_all()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Fix Berhasil',
                'message': 'Move %s berhasil direlasikan ke SOL %s.' % (
                    self.move_id.id, fixed[0]
                ),
                'type': 'success',
                'sticky': False,
            }
        }

    def action_fix_selected(self):
        """Fix semua records yang dipilih (dari Action menu multi-select)."""
        if not self:
            raise UserError("Pilih minimal 1 record.")

        fixed, skipped = self._do_fix()

        if not fixed:
            raise UserError("Tidak ada yang berhasil difix.\n\n" + "\n".join(skipped))

        # Recompute semua SOL terkait sekaligus
        sol_records = self.env['sale.order.line'].browse(list(set(fixed)))
        sol_records.invalidate_recordset()
        sol_records._compute_qty_delivered()
        sol_records.modified(['qty_delivered'])
        self.env.flush_all()

        msg = "Berhasil fix %d move(s)." % len(fixed)
        if skipped:
            msg += "\n\nDilewati:\n" + "\n".join(skipped)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Fix Orphan Moves',
                'message': msg,
                'type': 'success' if not skipped else 'warning',
                'sticky': True,
            }
        }
