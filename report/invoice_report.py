from odoo import models, fields, api

from odoo import models

import xlsxwriter

# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('hello.xlsx')

# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()

# Use the worksheet object to write
# data via the write() method.
worksheet.write('A1', 'Hello..')
worksheet.write('B1', 'Geeks')
worksheet.write('C1', 'For')
worksheet.write('D1', 'Geeks')

# Finally, close the Excel file
# via the close() method.
workbook.close()


class PartnerXlsx(models.AbstractModel):
    # _name = "report_invoice_report_data_xlsx"
    _inherit = 'report.report_xlsx.abstract'
    # workbook = xlsxwriter.Workbook('hello.xlsx')

    def generate_xlsx_report():
        sheet = workbook.add_worksheet('invoiceexample.exe')
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, "DOne", bold)
