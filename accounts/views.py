from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import FormView,View,ListView
from .forms import registaionForm,UpdateForm
from books.models import Book,BorrowBook
from django.contrib.auth import login,logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView



class RegistrationView(FormView):
    template_name = 'registration.html'
    form_class = registaionForm
    success_url = reverse_lazy('home')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form) 

# Create your views here.
    

class AccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
        return render(request, self.template_name, {'form': form})   


class UserLogin(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('update_profile')

class UserLogout(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')
 
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'profile.html'
    context_object_name = 'borrow'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = BorrowBook.objects.filter(user_id=user_id)
        return queryset
