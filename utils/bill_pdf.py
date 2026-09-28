from io import BytesIO
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle)

def build_bill_pdf(company, bill_rows, output_path=None):

    if not bill_rows:
        raise ValueError("No bill data available.")

    first = bill_rows[0]
    bill_number = first["bill_number"]
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    center_style = styles["Normal"]
    center_style.alignment = TA_CENTER
    right_style = styles["Normal"]
    right_style.alignment = TA_RIGHT
    story = []

    company_name = (company.get("company_name"))

    story.append(Paragraph(company_name, title_style))

    address = ", ".join(
        str(x)
        for x in [
            company.get("address"),
            company.get("city"),
            company.get("state"),
            company.get("pincode")
        ]
        if x
    )

    if address:
        story.append(Paragraph(address, center_style))

    contact = []

    if company.get("phone"):
        contact.append(f"Phone: {company['phone']}")

    if company.get("email"):
        contact.append(f"Email: {company['email']}")

    if company.get("gst_number"):
        contact.append(f"GST: {company['gst_number']}")

    if contact:
        story.append(Paragraph(" | ".join(contact), center_style))

    story.append(Spacer(1, 8))

    story.append(Paragraph("TAX INVOICE", styles["Heading1"]))

    story.append(Spacer(1, 6))

    customer_data = [
        [
            Paragraph(
                f"<b>Bill To:</b><br/>{first.get('customer_name') or '-'}<br/>{first.get('customer_phone') or '-'}",
                styles["Normal"]
            ),
            Paragraph(
                f"<b>Invoice No:</b> {bill_number}<br/>{'<b>Invoice Date:</b> ' + str(first['sale_date'])}",
                right_style
            )
        ]
    ]

    customer_table = Table(customer_data, colWidths=[110 * mm, 65 * mm])

    customer_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
        ])
    )

    story.append(customer_table)
    story.append(Spacer(1, 8))

    table_data = [["#", "Product", "Qty", "Unit", "Rate", "Amount"]]

    grand_total = 0
    total_quantity = 0

    for index, row in enumerate(bill_rows, start=1):
        quantity = int(row["quantity"])
        rate = float(row["selling_price"])
        amount = float(row["total_amount"])
        grand_total += amount
        total_quantity += quantity
        table_data.append(
            [
                str(index),
                row.get("product_name") or "Product",
                str(quantity),
                row.get("unit") or "-",
                f"{rate:,.2f}",
                f"{amount:,.2f}"
            ]
        )

    product_table = Table(
        table_data,
        colWidths=[10 * mm, 65 * mm, 17 * mm, 18 * mm, 30 * mm, 35 * mm],
        repeatRows=1
    )

    product_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (0, -1), "CENTER"),
            ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(product_table)
    story.append(Spacer(1, 10))

    total_table = Table(
        [
            ["Subtotal", f"₹ {grand_total:,.2f}"],
            ["Total Items", str(len(bill_rows))],
            ["Total Quantity", str(total_quantity)],
            ["GRAND TOTAL", f"₹ {grand_total:,.2f}"]
        ],
        colWidths=[130 * mm, 45 * mm]
    )

    total_table.setStyle(
        TableStyle([
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
            ("FONTSIZE", (0, 2), (-1, 2), 12),
            ("LINEABOVE", (0, 2), (-1, 2), 1, colors.black),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ])
    )

    story.append(total_table)
    story.append(Spacer(1, 20))
    story.append(Paragraph("Thank you for your business.", center_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("This invoice is generated electronically and is valid for official records.", styles["Italic"]))

    document.build(story)
    pdf_bytes = buffer.getvalue()
    return pdf_bytes

def save_bill_pdf(company_id, bill_number, company, bill_rows):

    pdf_bytes = build_bill_pdf(company, bill_rows, None)

    return None, pdf_bytes
