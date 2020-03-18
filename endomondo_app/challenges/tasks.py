from challenges.models.challenge import Challenge
from challenges.endomondo.api import EndomondoApi
from challenges.endomondo.challenge_page import ChallengePage
from mysite import settings
from django.http import HttpResponse


def process_page(api, ch, url):
    # TODO catch invalid challenge id
    html = api.get_page(url)
    with open('out.html', 'w') as file:
        file.write(html)
    page = ChallengePage(html)
    ch.update(page)
    return page


def fetch_challenges(request):
    api = EndomondoApi()
    print(settings.ENDOMONDO_USERNAME, settings.ENDOMONDO_PASSWORD)
    api.login(settings.ENDOMONDO_USERNAME, settings.ENDOMONDO_PASSWORD)

    challenges = Challenge.get_non_final()

    for ch in challenges:
        print('Updating challenge: {}'.format(ch.endomondo_id))
        url = 'https://www.endomondo.com/challenges/{}'.format(ch.endomondo_id)
        orig_page = process_page(api, ch, url)

        prev_url = orig_page.prev_page_url
        while prev_url is not None:
            page = process_page(api, ch, prev_url)
            prev_url = page.prev_page_url

        next_url = orig_page.next_page_url
        while next_url is not None:
            page = process_page(api, ch, next_url)
            prev_url = page.prev_page_url

    return HttpResponse()
