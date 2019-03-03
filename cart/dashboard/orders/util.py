from django.contrib.sessions.models import Session
from django.utils import timezone
from oscar.core.loading import get_model

Basket = get_model('basket', 'Basket')


def get_open_basket_sessions():
    """
    Return a list of sessions which contain an open or saved basket id
    """
    queryset = Session.objects.filter(
            expire_date__gt=timezone.now()).order_by(
                    '-expire_date')
    open_basket_sessions = []

    for session in queryset:
        session_data = session.get_decoded()

        try:
            # Only include sessions with basket_id in data
            basket = Basket.objects.get(session_data['submission']['basket_id'])

            # If the basket present hasn't been finalized, save it
            if basket.status in (Basket.OPEN, Basket.SAVED):
                open_basket_sessions.append(session)

        except:
            pass

    return open_basket_sessions

