from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import transaction
from .forms import DepositForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from books.models import Book,BorrowBook
from django.views import View
from django.utils import timezone
from django.shortcuts import redirect,get_object_or_404

def send_Mail(user,amount,mail_subject,template):
        message= render_to_string(template, {
                "user": user,
                "amount": amount,
            })
        send_email =EmailMultiAlternatives(mail_subject,"", to=[user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()


class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name = 'trans.html'
    model = transaction
    title = ''
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs  = super().get_form_kwargs()
        kwargs.update({'account': self.request.user.account})
        return kwargs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context.update({
            'title':self.title
        })
        return context
    

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_Mail(self.request.user,amount,'Deposit Message','email.html')
        return super().form_valid(form)
# Create your views here.
    
class BookBorrowView(LoginRequiredMixin, View):
    def get(self, request, id, **kwargs):
        book = get_object_or_404(Book, id=id)
        user = request.user

        if user.account.balance >= book.price:
            # Sufficient balance to borrow the book
            user.account.balance -= book.price
            user.account.save(update_fields=['balance'])

            BorrowBook.objects.create(
                book=book,
                user=user,
                date=timezone.now(),
            )

            messages.success(request, 'Book borrowed successfully.')
            send_Mail(self.request.user,book.book_name,'Borrow Book Message','email2.html')
            return redirect('profile')
        
        else:
            # Insufficient balance to borrow the book
            messages.warning(request, 'Insufficient balance to borrow the book. Please deposit.')
            return redirect('home')