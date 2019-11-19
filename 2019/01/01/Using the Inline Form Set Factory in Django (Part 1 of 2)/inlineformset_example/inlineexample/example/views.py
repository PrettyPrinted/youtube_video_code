from django.shortcuts import render, redirect
from .models import Programmer, Language
from django.forms import modelformset_factory, inlineformset_factory

def index(request, programmer_id):
    programmer = Programmer.objects.get(pk=programmer_id)
    #LanguageFormset = modelformset_factory(Language, fields=('name',))
    LanguageFormset = inlineformset_factory(Programmer, Language, fields=('name',))

    if request.method == 'POST':
        #formset = LanguageFormset(request.POST, queryset=Language.objects.filter(programmer__id=programmer.id))
        formset = LanguageFormset(request.POST, instance=programmer)
        if formset.is_valid():
            formset.save()
            #instances = formset.save(commit=False)
            #for instance in instances:
            #    instance.programmer_id = programmer.id 
            #    instance.save()

            return redirect('index', programmer_id=programmer.id)

    #formset = LanguageFormset(queryset=Language.objects.filter(programmer__id=programmer.id))
    formset = LanguageFormset(instance=programmer)

    return render(request, 'index.html', {'formset' : formset})