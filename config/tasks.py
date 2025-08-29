from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from redis import Redis

redis_client = Redis.from_url(settings.CELERY_BROKER_URL)


def get_email_lock_key(to_email, subject):
    """Генерация ключа блокировки для email задачи"""
    return f"email_lock:{subject}:{hash(frozenset(to_email))}"


@shared_task(
    name="send_email",
    bind=True,
    queue="emails",
    autoretry_for=(Exception,),
    retry_backoff=settings.EMAIL_TASK_RETRY_DELAY,
    retry_backoff_max=settings.EMAIL_TASK_STATE_TIMEOUT,
    max_retries=settings.EMAIL_TASK_MAX_RETRIES,
)
def send_email(self, subject, html_content, to_email):
    """
    Отправка HTML email с поддержкой блокировок и повторных попыток.
    """
    if not isinstance(to_email, list):
        to_email = [to_email]
    lock_key = get_email_lock_key(to_email, subject)
    try:
        if redis_client and redis_client.get(lock_key):
            return {
                "status": "skipped",
                "message": "Обнаружен дубликат задачи email",
                "recipients": to_email,
            }
        if redis_client:
            redis_client.set(
                lock_key,
                "processing",
                ex=settings.EMAIL_TASK_LOCK_TIMEOUT,
                nx=True,
            )
        email = EmailMultiAlternatives(
            subject=subject,
            body="Пожалуйста, включите HTML для просмотра этого сообщения.",
            from_email=settings.EMAIL_HOST_USER,
            to=to_email,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        return {
            "status": "success",
            "message": "Письмо отправлено",
            "recipients": to_email,
        }
    except Exception as e:
        raise self.retry(exc=e) from e
    finally:
        redis_client.delete(lock_key)
