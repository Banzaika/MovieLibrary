from django.db import models

class Contact(models.Model):
    email = models.EmailField(verbose_name='email')
    date = models.DateTimeField(verbose_name='Дата подписки', auto_now_add=True)

    def __str__(self):
        return self.email
