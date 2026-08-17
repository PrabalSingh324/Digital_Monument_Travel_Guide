"""
URL configuration for Digital_Monument_Travel_Guide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from explorebharat.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("about", about, name="about"),
    path("monuments", monuments, name="monuments"),
    path("gallery", gallery, name="gallery"),
    path("contact", contact, name="contact"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/", reset_password, name="reset_password"),
    path("dashboard", dashboard, name="dashboard"),
    path("add-monument", add_monument, name="add_monument"),
    path("view-monuments", view_monuments, name="view_monuments"),
    path("delete-monument/<int:pid>/", delete_monument, name="delete_monument"),
    path("edit-monument/<int:pid>/", edit_monument, name="edit_monument"),
    path("add-gallery/", add_gallery, name="add_gallery"),
    path("view-gallery/", view_gallery, name="view_gallery"),
    path("delete-gallery/<int:pid>/", delete_gallery, name="delete_gallery"),
    path("monument-details/<int:pid>/", monument_details, name="monument_details"),
    path("contact-messages/", contact_messages, name="contact_messages"),
    path("delete-contact/<int:pid>/", delete_contact, name="delete_contact"),
    path("registered-users/", registered_users, name="registered_users"),
    path("delete-user/<int:pid>/", delete_user, name="delete_user"),
    path("registered-users/", registered_users, name="registered_users"),
    path("delete-user/<int:pid>/", delete_user, name="delete_user"),
    path("logout/", logout, name="logout"),
    path("admin-login/", admin_login, name="admin_login"),
    path("book-ticket/<int:pid>/", book_ticket, name="book_ticket"),
    path(
    "book-ticket/<int:pid>/",
    book_ticket,
    name="book_ticket"
    ),
    path(
        "payment-success/",
        payment_success,
        name="payment_success"
    ),
    path(
    "view-bookings/",
    view_bookings,
    name="view_bookings"
    ),


    
    
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#Ye Django ko bolti hai:

"Development mode me (DEBUG=True) jo images media/ folder me hain, unhe browser me serve karo."

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
