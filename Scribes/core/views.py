from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView 

#Tells django which template to go to in order to render our SPA
class IndexTemplateView(LoginRequiredMixin, TemplateView):

    def get_template_names(self):
        template_name = "index.html"
        return template_name 