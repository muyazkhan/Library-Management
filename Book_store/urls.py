from django.contrib import admin
from django.urls import path,include
from core.views import BookView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('books/', include("books.urls")),
    path('transaction/', include("transaction.urls")),
    path('', BookView.as_view(),name='home'),
    path("books/<slug:book_slug>", BookView.as_view(), name="book_slug"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
