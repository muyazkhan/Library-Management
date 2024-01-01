from django.shortcuts import render
from django.views import View
from books.models import Book,category

class BookView(View):
    template_name = 'home.html'

    def get(self, request, book_slug=None):
        book = Book.objects.all()
        categories =category.objects.all()

        if book_slug is not None:
            Category = category.objects.get(slug=book_slug)
            book = Book.objects.filter(category=Category)

        return render(request, self.template_name, {"books": book, "categories": categories})