from django import forms
from .models import Cadre, Activity, Outline


class CreateNewParticipant(forms.Form):
    name = forms.CharField(label="Imię", max_length=30)
    surname = forms.CharField(label="Nazwisko", max_length=50)
    teams = [
        ("5 Podgórska Gromada Zuchowa „Magiczne Zuchy”", "5 Podgórska Gromada Zuchowa „Magiczne Zuchy”"),
        ("29 Podgórska Gromada Zuchowa „Jamanije”", "29 Podgórska Gromada Zuchowa „Jamanije”"),
        ("5 Podgórska Drużyna Harcerska „Eastwick” im. Zawiszy Czarnego", "5 Podgórska Drużyna Harcerska „Eastwick” im. Zawiszy Czarnego"),
        ("29 Podgórska Drużyna Harcerska „OMAN” im. hm. Olgi Drahonowskiej-Małkowskiej", "29 Podgórska Drużyna Harcerska „OMAN” im. hm. Olgi Drahonowskiej-Małkowskiej"),
        ("295 Podgórska Drużyna Wielopoziomowa „Fuzja”", "295 Podgórska Drużyna Wielopoziomowa „Fuzja”"),
        ("Kadra Pomocnicza", "Kadra Pomocnicza")
    ]

    team = forms.ChoiceField(
        choices=teams,
        label="Drużyna",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    cadre = forms.ModelChoiceField(
        queryset=Cadre.objects.all(),
        label="Opiekun",
        empty_label="Wybierz opiekuna",
        widget=forms.Select(attrs={"class": "form-select"})
    )



class CreateNewCadre(forms.Form):
    name = forms.CharField(label="Imię", max_length=30, required=True)
    surname = forms.CharField(label="Nazwisko", max_length=50, required=True)
    phone = forms.CharField(label="Numer Telefonu", max_length=9, required=False)
    email = forms.EmailField(label="Adres Mailowy", max_length=255, required=False)
    functions = [
        ("Komendant Całości","Komendant Całości"),
        ("Oboźny Całości","Oboźny Całości"),
        ("Komendant Podobozu StarszoHarcerskiego","Komendant Podobozu StarszoHarcerskiego"),
        ("Komendant Podobozu Harcerskiego","Komendant Podobozu Harcerskiego"),
        ("Komendant Podobozu Zuchowego","Komendant Podobozu Zuchowego"),
        ("Kwatermistrz","Kwatermistrz"),
        ("Magazynier","Magazynier"),
        ("Oboźny Podobozu StarszoHarcerskiego","Oboźny Podobozu StarszoHarcerskiego"),
        ("Oboźny Podobozu Harcerskiego","Oboźny Podobozu Harcerskiego"),
        ("Oboźny Podobozu Zuchowego","Oboźny Podobozu Zuchowego"),
        ("Programowy","Programowy"),
        ("Gość","Gość")
    ]

    function = forms.ChoiceField(
        choices=functions,
        label="Funkcja",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    


class CreateNewActivity(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["day", "block", "title", "desc", "person", "color"]

        labels = {
            "day": "Dzień",
            "block": "Blok programowy",
            "title": "Tytuł",
            "desc": "Opis",
            "person": "Osoba odpowiedzialna",
            "color": "Kolor zadania",
        }

        widgets = {
            "day": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["day"].input_formats = ["%Y-%m-%d"]


class AddNewOutline(forms.ModelForm):
    class Meta:
        model = Outline
        fields =["filename", "author", "file"]

        labels = {
            "filename": "Nazwa Konspektu",
            "author": "Autor Konspektu",
            "file": "Wybierz plik"
        }
