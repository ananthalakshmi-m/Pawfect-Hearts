from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
class SendGridPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends password reset email via SendGrid instead of SMTP.
        """
        reset_url = f"{context['protocol']}://{context['domain']}/users/reset/{context['uid']}/{context['token']}/"

        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <p>Hello,</p>
                <p>You requested a password reset for your Pawfect Hearts account.</p>
                <p>Click the link below to reset your password:</p>
                <p><a href="{reset_url}">{reset_url}</a></p>
                <p>If you didn’t request this, you can ignore this email safely.</p>
                <p style="color: #d63384;">With love,<br>Team Pawfect Hearts 🐶❤️</p>
            </body>
        </html>
        """

        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=to_email,
            subject="🐾 Pawfect Hearts Password Reset",
            html_content=html_message
        )
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)