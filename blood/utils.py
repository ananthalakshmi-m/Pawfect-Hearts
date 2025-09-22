import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_blood_request_email(to_email, blood_type_needed, dog_name):
    subject = "🐾 Urgent Dog Blood Request - Pawfect Hearts"

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <p>Hello,</p>
            <p>You’re receiving this email because your dog <strong>{dog_name}</strong> is registered as a donor with blood type <strong>{blood_type_needed}</strong>.</p>
            <p><strong>A new blood request</strong> has been posted that matches your dog’s blood type.</p>
            <p>Please log in to <a href="https://anantha-lakshmi-m.github.io/pawfect_hearts/">Pawfect Hearts</a> to view the request and see how you can help.</p>
            <p>Thank you for being a life-saving donor!</p>
            <p style="color: #d63384;">With love,<br>Team Pawfect Hearts 🐶❤️</p>
        </body>
    </html>
    """

    message = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_message
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
