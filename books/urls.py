
from django.urls import path
from .import views

urlpatterns = [
  path('details/<int:id>/', views.BookDetailsView.as_view(), name='book_details'),
  path('review/<int:id>/', views.BookReviewView.as_view(), name='book_review'),
  path('return/<int:id>',views.ReturnView.as_view(),name='return_book')

]
  