
from django.urls import path
from .views import DepositMoneyView,BookBorrowView


urlpatterns = [
  path('deposit/',DepositMoneyView.as_view(),name='deposit'),
  path('borrow_book/<int:id>/', BookBorrowView.as_view(), name='borrow_book'),
]