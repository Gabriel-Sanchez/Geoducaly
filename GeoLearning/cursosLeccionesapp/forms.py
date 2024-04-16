from django.forms import formset_factory
from django import forms
from .models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    # id : forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Quiz
        fields = (
            'name',
            'difficluty',
            'lessson',
            'required_score_to_pass',
            'time',
            
            # 'fk_grupo',
            # 'id'
        )
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control' }),
        }
    # def __init__(self, *args, **kwargs):
    #     super(QuizForm, self).__init__(*args, **kwargs)
    #     if self.instance and self.instance.id:
    #         self.fields['id'].initial = self.instance.id
    
    # lessson = forms.ChoiceField(choices=(), required=True)

    def __init__(self, *args, **kwargs):
        producto_choices = kwargs.pop('lessson_choices', None)
        super().__init__(*args, **kwargs)
        if producto_choices:
            self.fields['lessson'].choices = producto_choices
        
class QuestionForm(forms.ModelForm):
    
    text_n = forms.CharField(initial='0', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})  ) 
    
    opcion_1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})  ) 
    opcion_1_check = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control-quiz', 'onchange': 'uncheckOthers(this)','data-form-index':'{{ forloop.index }}'})) 
    opcion_1_n = forms.CharField(initial='0',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'})  ) 
    
    opcion_2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}) )
    opcion_2_check = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control-quiz', 'onchange': 'uncheckOthers(this)','data-form-index':'{{ forloop.index }}'})) 
    opcion_2_n = forms.CharField(initial='0',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}) )
    
    opcion_3 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}) ) 
    opcion_3_check = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control-quiz', 'onchange': 'uncheckOthers(this)','data-form-index':'{{ forloop.index }}'})) 
    opcion_3_n = forms.CharField(initial='0',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}) ) 
    
    opcion_4 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}) )
    opcion_4_check = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control-quiz', 'onchange': 'uncheckOthers(this)','data-form-index':'{{ forloop.index }}'})) 
    opcion_4_n = forms.CharField(initial='0', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}) )
    class Meta:
        model = Question
        fields = (
            'text',
            # 'quiz' 
        )
        widgets = {
          'opcion_1': forms.TextInput(attrs={'class': 'form-control','onchange':"uncheckOthers(this)" }),
          'opcion_1_n': forms.TextInput(attrs={'class': 'form-control','onchange':"uncheckOthers(this)" }),
          'opcion_1_check': forms.CheckboxInput(attrs={'class': 'form-control-quiz','onchange':"uncheckOthers(this)"}),
          
          'opcion_2': forms.TextInput(attrs={'class': 'form-control'}),
          'opcion_2_n': forms.TextInput(attrs={'class': 'form-control'}),
          'opcion_2_check': forms.CheckboxInput(attrs={'class': 'form-control-quiz','onchange':"uncheckOthers(this)"}),
          
          'opcion_3': forms.TextInput(attrs={'class': 'form-control'}),
          'opcion_3_n': forms.TextInput(attrs={'class': 'form-control'}),
          'opcion_3_check': forms.CheckboxInput(attrs={'class': 'form-control-quiz','onchange':"uncheckOthers(this)"}),
          
          'opcion_4': forms.TextInput(attrs={'class': 'form-control'}),
          'opcion_4_n': forms.TextInput(attrs={'class': 'form-control'}),
          'opcion_4_check': forms.CheckboxInput(attrs={'class': 'form-control-quiz','onchange':"uncheckOthers(this)"}),
          'text': forms.TextInput(attrs={'class': 'form-control'}),
          'text_n': forms.TextInput(attrs={'class': 'form-control'}),
      }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = (
                'text',
                # 'correct', 
                # 'question'
        )

class QuizForm2(forms.Form):
    name = forms.CharField(max_length=120, required=False)
    topic = forms.CharField(max_length=120, required=False)
    number_of_questions = forms.IntegerField(required=False)
    time = forms.IntegerField(help_text="duration of the quiz in minutes", required=False)
    required_score_to_pass = forms.IntegerField(help_text="required score in %", required=False)
    difficluty = forms.CharField(max_length=6, required=False)
    lessson = forms.IntegerField(required=False)
    fk_grupo = forms.IntegerField(required=False)

class MiFormulario(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)

MiFormSet = formset_factory(MiFormulario, extra=4)


from django.forms import formsets

class BaseExtraFormSet(formsets.BaseFormSet):
    pass


class ExtraForm(forms.Form):
    nombre = forms.CharField(max_length=100)


class NameForm(forms.Form):
    name = forms.CharField()
    apellido = forms.CharField(max_length=100)
    

# forms.py

from .models import Grupo, course


class GrupoForm_CRUD(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=115)
    #course = forms.ModelChoiceField(queryset=course.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=100,widget=forms.Textarea(attrs={'class': 'form-control','style': ' height: 60px;'}))
    # profesor = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    privado = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    imagen_grupo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Grupo
        fields = ['id','name','description', 'privado', 'imagen_grupo']
       
        widgets = {
            'profesor': forms.HiddenInput(),  
        }

# from .models import GrupoEstudiante

# class GrupoEstudianteForm(forms.ModelForm):
#     class Meta:
        
#         def __init__(self, grupos_filtrados, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.fields['grupo'].queryset = grupos_filtrados
        
#         model = GrupoEstudiante
#         fields = ['grupo', 'estudiante']
#         widgets = {
#             'estudiante': forms.HiddenInput(), 
#         }
        
        
from django import forms
from .models import Grupo, Profesor

class GrupoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        profesor_id = kwargs.pop('profesor_id')
        super(GrupoForm, self).__init__(*args, **kwargs)
        self.fields['grupo'] = forms.ModelChoiceField(
            queryset=Grupo.objects.filter(profesor__user=profesor_id),
            widget=forms.Select(attrs={'class': 'form-control'})
        )


class GrupoForm_estudiante(forms.Form):
    def __init__(self, *args, **kwargs):
        grupo_id = kwargs.pop('grupo_id')
        super(GrupoForm_estudiante, self).__init__(*args, **kwargs)
        self.fields['grupo'] = forms.ModelChoiceField(
            queryset=Grupo.objects.filter(id__in=grupo_id.values_list('grupo', flat=True)),
            widget=forms.Select(attrs={'class': 'form-control'})
        )