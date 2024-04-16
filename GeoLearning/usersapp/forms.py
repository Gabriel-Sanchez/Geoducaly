
from django import forms

class ProfileForm(forms.Form):
    firstname = forms.CharField(max_length=30, required=False)
    lastname = forms.CharField(max_length=30, required=False)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    country = forms.CharField(max_length=30, required=False)
    city = forms.CharField(max_length=30, required=False)

    # firstname = forms.CharField(max_length=30, required=True)
    # lastname = forms.CharField(max_length=30, required=True)
    # biography = forms.CharField(max_length=500, required=True)
    # phone_number = forms.CharField(max_length=20, required=True)
    # country = forms.CharField(max_length=30, required=True)
    # city = forms.CharField(max_length=30, required=True)
 
class ProfileFormImage(forms.Form):
    picture = forms.ImageField()

class ProfileFormPass(forms.Form):
    currentPass = forms.CharField(max_length=500, required=True)
    newPass = forms.CharField(max_length=500, required=True)
    confirmPass = forms.CharField(max_length=500, required=True)

class ProfileFormUserE(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.CharField(max_length=100, required=True)
    
    
from django import forms
from ciertoFalsoapp.models import Pregunta, test_True_false

class PreguntaForm(forms.ModelForm):
    imagen = forms.ImageField(required=False , widget=forms.FileInput)
    eliminar = forms.BooleanField(required=False, widget=forms.HiddenInput())
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    texto = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'})  ) 
    class Meta:
        model = Pregunta
        # fields = ['texto', 'es_verdadera', 'imagen']
        fields = ['id','texto', 'es_verdadera','imagen', 'eliminar']

class TestForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})  ) 
    class Meta:
        model = test_True_false
        # fields = ['name', 'leccion', 'grupofk']
        fields = ['name']



from django import forms
from juegosapp.models import Lesson_cards, CardPar

class LessonCardsForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})  ) 
    class Meta:
        model = Lesson_cards
        fields = ['name']

class CardParForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)
    # eliminar = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=False)
    eliminar = forms.BooleanField(required=False, widget=forms.HiddenInput())
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(required=False,max_length=100,  widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'})  ) 
    class Meta:
        model = CardPar
        fields = [ 'id','name', 'image']
