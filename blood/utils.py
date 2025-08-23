from django.core.mail import send_mail

def send_blood_request_email(to_email, blood_type_needed, dog_name):
    subject = "🐾 Urgent Dog Blood Request - Pawfect Hearts"
    
    plain_message = (
        f"Hello,\n\n"
        f"You’re receiving this email because your dog {dog_name} is registered as a donor with blood type {blood_type_needed}.\n\n"
        "A new blood request has been posted that matches your dog’s blood type.\n\n"
        "Please log in to Pawfect Hearts to view the request and see how you can help.\n\n"
        "Thank you for being a life-saving donor!\n\n"
        "With love,\n"
        "Team Pawfect Hearts 🐶❤️"
    )

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <p>Hello,</p>
            <p>You’re receiving this email because your dog <strong>{dog_name}</strong> is registered as a donor with blood type <strong>{blood_type_needed}</strong>.</p>
            <p><strong>A new blood request</strong> has been posted that matches your dog’s blood type.</p>
            <p>Please log in to <a href="https://pawfect-hearts.onrender.com">Pawfect Hearts</a> to view the request and see how you can help.</p>
            <p>Thank you for being a life-saving donor!</p>
            <p style="color: #d63384;">With love,<br>Team Pawfect Hearts 🐶❤️</p>
        </body>
    </html>
    """

    send_mail(
        subject,
        plain_message,
        None,
        [to_email],
        html_message=html_message
    )
