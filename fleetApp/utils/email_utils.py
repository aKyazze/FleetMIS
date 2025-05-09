from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

def send_notification(subject, template_name, context, recipient_email):
    message_html = render_to_string(template_name, context)

    # Create email object
    email = EmailMultiAlternatives(
        subject=subject,
        body=message_html,  # fallback plain text version
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )

    email.attach_alternative(message_html, "text/html")
    email.send()
