from django import template
from blog.models import Category

register = template.Library()

@register.simple_tag()
def get_categories():
   categories = Category.objects.all()
   return categories


@register.simple_tag()
def get_sorters():
   sorters = {
      '-views': 'По просмотрам+',
      'views': 'По просмотрам-',
      '-title': 'По алфавиту+',
      'title': 'По алфавиту-',
      '-created_at': 'Создан+',
      'created_at': 'Создан-'
   }
   return sorters
