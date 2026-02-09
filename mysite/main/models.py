from django.db import models
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.


class Cadre(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    phone = models.CharField(max_length=9)
    email = models.EmailField(max_length=255)
    function = models.CharField(max_length=30)


    def __str__(self):
        return f"{self.name} {self.surname}"
    

class Participants(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    team = models.CharField(max_length=50)
    cadre = models.ForeignKey(Cadre, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    

class Activity(models.Model):

    BLOCKS = [
        ("rano", "Rano"),
        ("przedpołudniem", "Przedpołudniem"),
        ("popołudniu", "Popołudniu"),
        ("wieczorem", "Wieczorem"),
    ]

    COLOUR = [
        ("#2e8746", "Zielony"),
        ("#940f0a", "Czerwony"),
        ("#263999", "Niebieski"),
        ("#3a79b0", "Błękitny"),
        ("#663294", "Fioletowy"),
        ("#c73aaf", "Różowy"),
        ("#c7793a", "Pomarańczowy"),
        ("#a2a825", "Żółty"),
        ("#63635b", "Szary"),
    ]

    day = models.DateField()
    block = models.CharField(max_length=20, choices=BLOCKS)
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500, null = True, blank=True)
    person = models.ForeignKey(Cadre, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(max_length=50, choices=COLOUR)

    def __str__(self):
        return f"{self.day} - {self.block}: {self.title}"
    


class Outline(models.Model):
    filename = models.CharField(max_length=50)
    author = models.ForeignKey(Cadre, on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='outlines/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'jpg', 'png','odt', 'jpeg'])])
    uploaded_at = models.DateTimeField(auto_now_add=True)



class Payments(models.Model):
    participant = models.ForeignKey(Participants, on_delete=models.CASCADE, related_name='payments')
    installment = models.CharField(max_length=20, default="Niezapłacono")
    entire_amount = models.CharField(max_length=20, default ="Niezapłacono")

@receiver(post_save, sender = Participants)
def create_payment_for_participant(sender, instance, created, **kwargs):
    if created:
        Payments.objects.create(participant=instance)
