from .models import CategoryTagModel, AuthorModel


class DataMixin:

    def get_category(self, **kwargs):
        context = kwargs
        context['category'] = CategoryTagModel.objects.all().prefetch_related('tag')
        return context

    def get_authors(self, **kwargs):
        context = kwargs
        context['authors'] = AuthorModel.objects.all().order_by('-staff').select_related('staff')
        return context
