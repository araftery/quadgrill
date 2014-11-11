from core.tasks import send_text as send_text_task


def send_text(template_name, recipient, context):
    send_text_task(template_name, recipient, context)
