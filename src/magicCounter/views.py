from django.shortcuts import render
from datetime import datetime

def index(request):
    date = datetime.today()
    return render(request, "magicCounter/base.html", context={
        "prenom": "laurent",
        "date": date
    })