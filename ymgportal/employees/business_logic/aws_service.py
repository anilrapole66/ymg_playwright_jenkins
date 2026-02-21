import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage


# Sender (must be allowed/verified in ACS Email)
SENDER = os.getenv("MAIL_SENDER", "DoNotReply@ymgit.com")
EMAIL_BRAND_NAME = "YM Global"
EMAIL_LOGO_PATH = "media/YMGIT_Name_board_logo.png"

ACS_SMTP_HOST = os.getenv("ACS_SMTP_HOST", "smtp.azurecomm.net")
ACS_SMTP_PORT = int(os.getenv("ACS_SMTP_PORT", "587"))
ACS_SMTP_USER = os.getenv("ACS_SMTP_USER")
ACS_SMTP_PASS = os.getenv("ACS_SMTP_PASS")


def _send_via_acs_smtp(msg, sender: str, recipients: list[str]):
    """
    Sends a pre-built MIME message via Azure Communication Services Email (SMTP AUTH).
    """
    if not ACS_SMTP_USER or not ACS_SMTP_PASS:
        raise RuntimeError("Missing ACS SMTP credentials. Set ACS_SMTP_USER and ACS_SMTP_PASS in .env")

    # Ensure headers exist (some callers might not set them)
    msg["From"] = msg.get("From") or sender
    msg["To"] = msg.get("To") or ", ".join(recipients)

    with smtplib.SMTP(ACS_SMTP_HOST, ACS_SMTP_PORT, timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(ACS_SMTP_USER, ACS_SMTP_PASS)
        server.sendmail(sender, recipients, msg.as_string())


def send_email_with_attachment_old(recipient, filename, file_bytes):
    msg = MIMEMultipart()
    msg["Subject"] = "Timesheet Export"
    msg["From"] = SENDER
    msg["To"] = recipient

    msg.attach(MIMEText("Attached is the timesheet export.", "html"))

    attachment = MIMEApplication(file_bytes)
    attachment.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(attachment)

    _send_via_acs_smtp(msg, SENDER, [recipient])


def send_email_with_attachment(recipient, filename, file_bytes, table_rows=None):
    # Convert table rows to HTML table
    table_html = ""
    if table_rows:
        table_html = """
        <table style="width:100%; border-collapse: collapse; margin-top:20px;">
            <thead>
                <tr style="background:#1976d2; color:white;">
                    <th style="padding:10px; border:1px solid #ddd;">Employee Name</th>
                    <th style="padding:10px; border:1px solid #ddd;">Month & Year</th>
                    <th style="padding:10px; border:1px solid #ddd;">Approve / Reject</th>
                </tr>
            </thead>
            <tbody>
        """
        for row in table_rows:
            table_html += f"""
                <tr style="text-align:center;">
                    <td style="padding:10px; border:1px solid #ddd;">{row['name']}</td>
                    <td style="padding:10px; border:1px solid #ddd;">{row['month_year']}</td>
                    <td style="padding:10px; border:1px solid #ddd; height:30px;"></td>
                </tr>
            """
        table_html += "</tbody></table>"

    # Load logo (ensure this path exists on your runtime machine)
    with open(EMAIL_LOGO_PATH, "rb") as f:
        logo_bytes = f.read()

    # MIME Root
    msg_root = MIMEMultipart("related")
    msg_root["Subject"] = "Timesheet Export"
    msg_root["From"] = SENDER
    msg_root["To"] = recipient

    # Alternative (plain + html)
    msg_alternative = MIMEMultipart("alternative")
    msg_root.attach(msg_alternative)

    # Fallback text
    msg_alternative.attach(MIMEText("Your timesheet export is attached.\n", "plain"))

    # HTML Content
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="text-align:center;">
                <img src="cid:logoimage" style="width:160px; margin-bottom:20px;" />
            </div>

            <h2 style="text-align:center; color:#333;">{EMAIL_BRAND_NAME} Timesheet Export Summary</h2>

            <p style="font-size:15px; color:#444;">Hello,</p>

            <p style="font-size:15px; color:#444;">
                Please find attached the ZIP file containing the selected timesheets.
                Below is the summary of employees included.
            </p>

            {table_html}

            <p style="font-size:14px; color:#888; margin-top:30px;">
                Regards,<br>
                <b>{EMAIL_BRAND_NAME}</b>
            </p>
        </body>
    </html>
    """
    msg_alternative.attach(MIMEText(html_content, "html"))

    # Inline Image
    img = MIMEImage(logo_bytes)
    img.add_header("Content-ID", "<logoimage>")
    img.add_header("Content-Disposition", "inline", filename="YMGIT_Name_board_logo.png")
    msg_root.attach(img)

    # Attachment
    attachment = MIMEApplication(file_bytes)
    attachment.add_header("Content-Disposition", "attachment", filename=filename)
    msg_root.attach(attachment)

    _send_via_acs_smtp(msg_root, SENDER, [recipient])


# Backward-compatible alias used by existing views/imports.
def send_ses_email_with_attachment(recipient, filename, file_bytes, table_rows=None):
    return send_email_with_attachment(
        recipient=recipient,
        filename=filename,
        file_bytes=file_bytes,
        table_rows=table_rows,
    )


def send_password_reset_email(recipient, reset_url):
    with open(EMAIL_LOGO_PATH, "rb") as f:
        logo_bytes = f.read()

    msg_root = MIMEMultipart("related")
    msg_root["Subject"] = "Reset Your Password"
    msg_root["From"] = SENDER
    msg_root["To"] = recipient

    msg_alt = MIMEMultipart("alternative")
    msg_root.attach(msg_alt)

    html_body = f"""
    <html>
    <body style="font-family:Arial,sans-serif;background:#f8fafc;padding:30px;">
        <div style="max-width:520px;margin:auto;background:white;
                    border-radius:12px;padding:30px;">
            <div style="text-align:center;">
                <img src="cid:logoimage" style="width:150px;">
            </div>

            <h2 style="text-align:center;">Reset Your Password</h2>

            <p>Click the button below to reset your password:</p>

            <div style="text-align:center;margin:30px 0;">
                <a href="{reset_url}"
                   style="background:#1883b7;color:white;
                          padding:12px 22px;border-radius:10px;
                          text-decoration:none;font-weight:600;">
                    Reset Password
                </a>
            </div>

            <p style="font-size:13px;color:#777;">
                If you didn’t request this, you can ignore this email.
            </p>

            <p style="font-size:13px;color:#999;">
                — {EMAIL_BRAND_NAME}
            </p>
        </div>
    </body>
    </html>
    """
    msg_alt.attach(MIMEText(html_body, "html"))

    img = MIMEImage(logo_bytes)
    img.add_header("Content-ID", "<logoimage>")
    msg_root.attach(img)

    _send_via_acs_smtp(msg_root, SENDER, [recipient])
