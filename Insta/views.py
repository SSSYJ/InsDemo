from django.views.generic import TemplateView

class HelloWorld(TemplateView): # HelloWorld is-a TempateView
    template_name = 'test.html'