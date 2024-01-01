from django.shortcuts import render,redirect ,get_object_or_404
from django.urls import reverse_lazy
from .forms import ReviewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book,review,category,BorrowBook
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView,ListView,CreateView
from transaction.views import send_Mail
class homeview(ListView):
    template_name = "home.html"
    context_object_name = "books"
    model = Book

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.kwargs:
            slug = self.kwargs['book_slug']
            category = category.objects.get(slug=slug)
            queryset = super().get_queryset().filter(categories=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = category.objects.all()
        context.update({"category": categories})
        return context
    
class BookDetailsView(LoginRequiredMixin,DetailView):
    template_name = "book_details.html"
    model = Book
    pk_url_kwarg = "id"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        book = Book.objects.get(pk=id)
        reviews = review.objects.filter(book=book)
        context.update({'reviews': reviews})
            
        return context


class BookReviewView(LoginRequiredMixin, CreateView):
    template_name = "book_review.html"
    model = review
    form_class = ReviewForm
    success_url = reverse_lazy("profile")

    def get_initial(self):
        id = self.kwargs['id']
        book = Book.objects.get(pk=id)
        initial = {'book': book, 'user': self.request.user}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        book = Book.objects.get(pk=id)
        context.update({
            'book': book
        })
        return context

    def form_valid(self, form):
        id = self.kwargs['id']
        book = Book.objects.get(pk=id)
        is_already_reviewed = review.objects.filter(
            book=book, user=self.request.user).count()
        if is_already_reviewed >= 1:
            messages.info(self.request, "You have already reviewed this book.")
            return redirect("profile")
        else:
            messages.success(self.request, "Thanks for your valuable review.")
        return super().form_valid(form)
    


class ReturnView(LoginRequiredMixin, View):
    def get(self,request,id, **kwargs):
        book = get_object_or_404(BorrowBook, id = id)
        user = self.request.user
        user.account.balance += book.book.price
        messages.success(request, 'book return successful')
        user.account.save(update_fields=['balance'])
        book.delete()
        return redirect('profile')