from django.http import HttpResponseRedirect
from .tasks import send_message2boss
from .models import Contact


def create_contact(request):
    address = request.POST['Email']
    contact = Contact.objects.create(email=address)
    contact.save()
    send_message2boss.delay()
    return HttpResponseRedirect('/')
