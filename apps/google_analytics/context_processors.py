from django.conf import settings


def ga_code(request):
    return {
        'GA_CODE': settings.GA_CODE
    }
