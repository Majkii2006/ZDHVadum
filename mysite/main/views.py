from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from .models import Participants, Cadre, Activity, Outline, Payments
from .forms import CreateNewParticipant, CreateNewCadre, CreateNewActivity, AddNewOutline
from datetime import date, timedelta, datetime
from django.db.models import Q

# Create your views here.


def index(response):
    return render(response, 'main/base.html', {})


def home(response):
    return render(response, 'main/home.html', {})


def person(response):
    return render(response, 'main/person.html', {})



def schedule(request):
    today = date.today()

    # Tydzień 1
    monday1 = today - timedelta(days=today.weekday())
    days1 = [monday1 + timedelta(days=i) for i in range(7)]

    # Tydzień 2
    monday2 = monday1 + timedelta(days=7)
    days2 = [monday2 + timedelta(days=i) for i in range(7)]

    blocks = ["rano", "przedpołudniem", "popołudniu", "wieczorem"]

    # Pobranie aktywności
    activities = Activity.objects.filter(day__range=[days1[0], days2[-1]])

    # Siatki
    grid1 = {day: {b: None for b in blocks} for day in days1}
    grid2 = {day: {b: None for b in blocks} for day in days2}

    for a in activities:
        if a.day in grid1:
            grid1[a.day][a.block] = a   # ← TU ZMIANA
        elif a.day in grid2:
            grid2[a.day][a.block] = a   # ← TU ZMIANA

    week1 = []
    for block in blocks:
        row = [(day, grid1[day][block]) for day in days1]
        week1.append((block, row))

    week2 = []
    for block in blocks:
        row = [(day, grid2[day][block]) for day in days2]
        week2.append((block, row))

    return render(request, "main/schedule.html", {
        "today": today,
        "days1": days1,
        "days2": days2,
        "week1": week1,
        "week2": week2,
    })



def add_schedule(request):
    day_str = request.GET.get("day")
    block = request.GET.get("block")

    # konwersja string → date
    day = None
    if day_str:
        try:
            day = datetime.strptime(day_str, "%Y-%m-%d").date()
        except ValueError:
            day = None

    if request.method == "POST":
        form = CreateNewActivity(request.POST)
        if form.is_valid():
            form.save()
            return redirect("schedule")

    else:

        form = CreateNewActivity(initial={
            "day": day,
            "block": block,
        })

    return render(request, "main/addschedule.html", {
        "form": form,
    })


def delete_schedule(request, id):
    activity = Activity.objects.filter(id=id).first()
    activity.delete()
    return redirect('schedule')

def docs(response):
    return render(response, 'main/docs.html', {})


def cadre(response):
    cadre = Cadre.objects.all()
    komendant_calosci = Cadre.objects.filter(function="Komendant Całości").values_list("name", "surname").first()
    obozny_calosci = Cadre.objects.filter(function="Oboźny Całości").values_list("name", "surname").first()
    komendant_hs = Cadre.objects.filter(function="Komendant Podobozu StarszoHarcerskiego").values_list("name", "surname").first()
    obozny_hs = Cadre.objects.filter(function="Obożny Podobozu StarszoHarcerskiego").values_list("name", "surname").first()
    komendant_h = Cadre.objects.filter(function="Komendant Podobozu Harcerskiego").values_list("name", "surname").first()
    obozny_h = Cadre.objects.filter(function="Oboźny Podobozu Harcerskiego").values_list("name", "surname").first()
    komendant_z = Cadre.objects.filter(function="Komendant Podobozu Zuchowego").values_list("name", "surname").first()
    obozny_z = Cadre.objects.filter(function="Oboźny Podobozu Zuchowego").values_list("name", "surname").first()
    kwatermistrz = Cadre.objects.filter(function="Kwatermistrz").values_list("name", "surname").first()

    liczba_komendant_calosci = Cadre.objects.filter(function="Komendant Całości").count()
    liczba_obozny_calosci = Cadre.objects.filter(function="Oboźny Całości").count()
    liczba_komendant_hs = Cadre.objects.filter(function="Komendant Podobozu StarszoHarcerskiego").count()
    liczba_obozny_hs = Cadre.objects.filter(function="Oboźny Podobozu StarszoHarcerskiego").count()
    liczba_komendant_h  = Cadre.objects.filter(function="Komendant Podobozu StarszoHarcerskiego").count()
    liczba_obozny_h = Cadre.objects.filter(function="Oboźny Podobozu Harcerskiego").count()
    liczba_komendant_z = Cadre.objects.filter(function="Komendant Podobozu Zuchowego").count()
    liczba_obozny_z = Cadre.objects.filter(function="Oboźny Podobozu Zuchowego").count()
    liczba_kwatermistrz = Cadre.objects.filter(function="Kwatermistrz").count()

    puste_numery = Cadre.objects.filter(phone="").count()




    if liczba_komendant_calosci > 1:
        ostrzezenie_komendant_calosci = "- Masz przypisanego więcej niż jednego Komendanta Całości"
    else:
        ostrzezenie_komendant_calosci = ""

    if liczba_obozny_calosci > 1:
        ostrzezenie_obozny_calosci = "- Masz przypisanego więcej niż jednego Oboźnego Całości"
    else:
        ostrzezenie_obozny_calosci = ""

    if liczba_komendant_hs > 1:
        ostrzezenie_komendant_hs = "- Masz przypisanego więcej niż jednego Komendanta HS"
    else:
        ostrzezenie_komendant_hs = ""

    if liczba_obozny_hs > 1:
        ostrzezenie_obozny_hs = "- Masz przypisanego więcej niż jednego Oboźnego HS"
    else:
        ostrzezenie_obozny_hs = ""

    if liczba_komendant_h > 1:
        ostrzezenie_komendant_h = "- Masz przypisanego więcej niż jednego Komendanta H"
    else:
        ostrzezenie_komendant_h = ""

    if liczba_obozny_h > 1:
        ostrzezenie_obozny_h = "- Masz przypisanego więcej niż jednego Oboźnego H"
    else:
        ostrzezenie_obozny_h = ""

    if liczba_komendant_z > 1:
        ostrzezenie_komendant_z = "- Masz przypisanego więcej niż jednego Komendanta Z"
    else:
        ostrzezenie_komendant_z = ""

    if liczba_obozny_z > 1:
        ostrzezenie_obozny_z = "- Masz przypisanego więcej niż jednego Oboźnego Z"
    else:
        ostrzezenie_obozny_z = ""

    if liczba_kwatermistrz > 1:
        ostrzezenie_kwatermistrz = "- Masz przypisanego więcej niż jednego Kwatermistrza"
    else:
        ostrzezenie_kwatermistrz = ""

    if puste_numery == 1:
        ostrzezenie_puste_numery = f"- Masz {puste_numery} brak w numerach telefonu przy kadrze"
    elif puste_numery>1 and puste_numery<5:
        ostrzezenie_puste_numery = f"- Masz {puste_numery} braki w numerach telefonu przy kadrze"
    elif puste_numery>=5:
        ostrzezenie_puste_numery = f"- Masz {puste_numery} braków w numerach telefonu przy kadrze"
    else:
        ostrzezenie_puste_numery = ""
    


    return render(response, 'main/cadre.html', {
        "cadre":cadre, 
        "komendant_calosci": komendant_calosci, 
        "obozny_calosci": obozny_calosci,
        "komendant_hs": komendant_hs,
        "obozny_hs": obozny_hs,
        "komendant_h": komendant_h,
        "obozny_h": obozny_h,
        "komendant_z": komendant_z,
        "obozny_z": obozny_z,
        "kwatermistrz": kwatermistrz,
        "ostrzezenie_komendant_calosci": ostrzezenie_komendant_calosci,
        "ostrzezenie_obozny_calosci": ostrzezenie_obozny_calosci,
        "ostrzezenie_komendant_hs": ostrzezenie_komendant_hs,
        "ostrzezenie_obozny_hs": ostrzezenie_obozny_hs,
        "ostrzezenie_komendant_h":ostrzezenie_komendant_h,
        "ostrzezenie_obozny_h": ostrzezenie_obozny_h,
        "ostrzezenie_komendant_z": ostrzezenie_komendant_z,
        "ostrzezenie_obozny_z": ostrzezenie_obozny_z,
        "ostrzezenie_kwatermistrz": ostrzezenie_kwatermistrz,
        "ostrzezenie_puste_numery": ostrzezenie_puste_numery
        })




def add_cadre(response):
    if response.method == "POST":
        form = CreateNewCadre(response.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            function = form.cleaned_data["function"]
            cadre = Cadre(name=name, surname=surname, phone=phone, email=email, function=function)
            cadre.save()
            return redirect('cadre')
        
    else:
        form = CreateNewCadre()
    return render(response, 'main/addcadre.html', {"form": form})


def edit_cadre(request, id):
    cadre = Cadre.objects.filter(id=id).first()

    if request.method == "POST":
        form = CreateNewCadre(request.POST)
        if form.is_valid():
            cadre.name = form.cleaned_data["name"]
            cadre.surname = form.cleaned_data["surname"]
            cadre.phone = form.cleaned_data["phone"]
            cadre.email = form.cleaned_data["email"]
            cadre.function = form.cleaned_data["function"]
            cadre.save()
            return redirect('cadre')
    else:
        form = CreateNewCadre(initial={
            "name": cadre.name,
            "surname": cadre.surname,
            "phone": cadre.phone,
            "email": cadre.email,
            "function": cadre.function,
        })

    return render(request, 'main/editcadre.html', {"form": form})



def delete_cadre(response, id):
    Cadre.objects.filter(id=id).delete()
    return redirect("cadre")
    
def participants(response):
    ls = Participants.objects.all()
    magiczne = Participants.objects.filter(team__contains="5 Podgórska Gromada Zuchowa „Magiczne Zuchy”").count()
    jamanije = Participants.objects.filter(team__contains="29 Podgórska Gromada Zuchowa „Jamanije”").count()
    eastwick = Participants.objects.filter(team__contains="5 Podgórska Drużyna Harcerska „Eastwick” im. Zawiszy Czarnego").count()
    oman = Participants.objects.filter(team__contains="29 Podgórska Drużyna Harcerska „OMAN” im. hm. Olgi Drahonowskiej-Małkowskiej").count()
    fuzja = Participants.objects.filter(team__contains="295 Podgórska Drużyna Wielopoziomowa „Fuzja”").count()
    pomocnicza = Participants.objects.filter(team__contains="Kadra Pomocnicza").count()


    cadre = Cadre.objects.all()
    for c in cadre:
        name = c.name
        surname = c.surname
        #DEBUGGING TROUBLES
        print(name, surname)
        numbers_of_cadre = Participants.objects.filter(cadre=f"{name} {surname}").count()

    return render(response, 'main/participants.html', 
                  {"ls":ls, 
                    "magiczne":magiczne, 
                    "jamanije":jamanije, 
                    "eastwick":eastwick, 
                    "oman":oman, 
                    "fuzja":fuzja, 
                    "pomocnicza":pomocnicza,
                    "cadre": cadre,
                    "numbers_of_cadre": numbers_of_cadre})

def add_participant(response):
    if response.method == "POST":
        form = CreateNewParticipant(response.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            surname = form.cleaned_data["surname"]
            team = form.cleaned_data["team"]
            cadre = form.cleaned_data["cadre"]
            participant = Participants(name=name, surname=surname, team = team, cadre = cadre)
            participant.save()
            return redirect("participants")
        

    else:
        form = CreateNewParticipant()
    return render(response, 'main/addparticipant.html', {"form": form})


def edit_participant(response, id):
    participant = Participants.objects.filter(id=id).first()

    if response.method == "POST":
        form = CreateNewParticipant(response.POST)
        if form.is_valid():
            participant.name = form.cleaned_data["name"]
            participant.surname = form.cleaned_data["surname"]
            participant.team = form.cleaned_data["team"]
            participant.cadre = form.cleaned_data["cadre"]
            participant.save()
            return redirect('participants')

    else:
        form = CreateNewParticipant(initial={
            "name": participant.name,
            "surname": participant.surname,
            "team": participant.team,
            "cadre": participant.cadre
        })

    return render(response, 'main/editparticipant.html', {"form": form})



def delete_participant(request, id):
    participant = Participants.objects.filter(id=id).first()
    participant.delete()
    return redirect('participants')



def outlines(response):
    outlines = Outline.objects.all()
    return render(response, 'main/outlines.html', {"outlines": outlines})


def add_outline(request):
    if request.method == "POST":
        form = AddNewOutline(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('outlines')
    else: 
        form = AddNewOutline()
    return render(request, 'main/addoutline.html', {"form": form})


def download_outline(request, id):
    outline = Outline.objects.get(id=id)
    file = open(outline.file.path, 'rb')
    response = FileResponse(file)
    filename = outline.file.name.split('/')[-1]
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
    

def show_outline(response, id):
    outline = get_object_or_404(Outline, id=id)
    return FileResponse(open(outline.file.path, 'rb'))
    

def delete_outline(response, id):
    outline = Outline.objects.filter(id=id).first()
    outline.delete()
    return redirect('outlines')
    

def payments(response):
    payments = Payments.objects.all()

    magiczne_zuchy = Payments.objects.filter(participant__team="5 Podgórska Gromada Zuchowa „Magiczne Zuchy”").filter(Q(installment="Niezapłacono") | Q(entire_amount = "Niezapłacono")).count()

    jamanije = Payments.objects.filter(participant__team="29 Podgórska Gromada Zuchowa „Jamanije”").filter(Q(installment="Niezapłacono") | Q(entire_amount = "Niezapłacono")).count()

    eastwick = Payments.objects.filter(participant__team="5 Podgórska Drużyna Harcerska „Eastwick” im. Zawiszy Czarnego").filter(Q(installment="Niezapłacono") | Q(entire_amount = "Niezapłacono")).count()

    oman = Payments.objects.filter(participant__team="29 Podgórska Drużyna Harcerska „OMAN” im. hm. Olgi Drahonowskiej-Małkowskiej").filter(Q(installment="Niezapłacono") | Q(entire_amount = "Niezapłacono")).count()

    fuzja = Payments.objects.filter(participant__team="295 Podgórska Drużyna Wielopoziomowa „Fuzja”").filter(Q(installment="Niezapłacono") | Q(entire_amount = "Niezapłacono")).count()

    kadra_pomocnicza = Payments.objects.filter(participant__team="Kadra Pomocnicza").filter(Q(installment="Niezapłacono") | Q(entire_amount = "Niezapłacono")).count()

    ilosc_uczestnikow = Payments.objects.all().count()


    

    return render(response, 'main/payments.html', 
                {"payments": payments, 
                "magiczne_zuchy": magiczne_zuchy, 
                "jamanije": jamanije, 
                "eastwick": eastwick, 
                "oman": oman,
                "fuzja": fuzja,
                "kadra_pomocnicza": kadra_pomocnicza,
                "ilosc_uczestnikow": ilosc_uczestnikow
                })


def installment(response, id):

    payment = get_object_or_404(Payments, id=id)

    if payment.installment == "Niezapłacono":
        payment.installment = "Zapłacono"
        payment.save()
    elif payment.installment == "Zapłacono":
        payment.installment = "Niezapłacono"
        payment.save()
    return redirect('payments')



def entire_amount(response, id):
    
    payment = get_object_or_404(Payments, id=id)
    if payment.entire_amount == "Niezapłacono":
        payment.entire_amount = "Zapłacono"
        payment.save()
    elif payment.entire_amount == "Zapłacono":
        payment.entire_amount = "Niezapłacono"
        payment.save()
    return redirect('payments')



