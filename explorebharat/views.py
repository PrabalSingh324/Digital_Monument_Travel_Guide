from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .models import Monument, Gallery
import razorpay
from django.conf import settings
from decimal import Decimal
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
# Create your views here.

def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")



def monuments(request):

    search = request.GET.get("search")

    monuments = Monument.objects.all()

    if search:
        monuments = monuments.filter(monument_name__icontains=search)

    featured_monument = Monument.objects.filter(is_featured=True).first()

    return render(request, "monuments.html", {
        "monuments": monuments,
        "featured_monument": featured_monument,
    })

def gallery(request):

    gallery = Gallery.objects.all()

    d = {
        "gallery": gallery,
    }

    return render(request, "gallery.html", d)

def contact(request):
    error = ""

    if request.method == "POST":

        n = request.POST['full_name']
        e = request.POST['email']
        s = request.POST['subject']
        m = request.POST['message']

        Contact.objects.create(full_name=n,email=e,subject=s,message=m)
        error = "no"
    d = {"error": error}
    return render(request, "contact.html", d)
   


def login(request):

    error = ""

    if request.method == "POST":

        em = request.POST['email']
        pw = request.POST['password']

        user = Register.objects.filter(email=em, password=pw)

        if user:
            request.session["user_email"] = em
            error = "no"
        else:

            error = "yes"

    d = {"error": error}

    return render(request, "login.html", d)


def register(request):

    error = ""

    if request.method == "POST":

        fn = request.POST['fullname']
        un = request.POST['username']
        em = request.POST['email']
        ph = request.POST['phone']
        pw = request.POST['password']
        cp = request.POST['confirm_password']
        gd = request.POST['gender']

        if pw == cp:

            if Register.objects.filter(email=em).exists():

                error = "email"

            elif Register.objects.filter(username=un).exists():

                error = "username"
    

            else:

                Register.objects.create(fullname=fn,username=un,email=em,phone=ph,password=pw,confirm_password=cp,gender=gd)

                error = "no"

        else:

            error = "notmatch"

    d = {'error': error}

    return render(request, "register.html", d)


from django.shortcuts import render, redirect
from .models import Register

def forgot_password(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")

        try:

            user = Register.objects.get(
                username=username,
                email=email
            )

            request.session["reset_user"] = user.id

            return redirect("reset_password")

        except Register.DoesNotExist:

            error = "yes"

    d = {
        "error": error
    }

    return render(request, "forgot_password.html", d)


def reset_password(request):

    if "reset_user" not in request.session:
        return redirect("forgot_password")

    user = Register.objects.get(id=request.session["reset_user"])

    error = ""

    if request.method == "POST":

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:

            user.password = new_password
            user.confirm_password = confirm_password
            user.save()

            del request.session["reset_user"]

            error = "no"

        else:

            error = "yes"

    d = {
        "error": error
    }

    return render(request, "reset_password.html", d)    



def add_monument(request):
    if not check_admin(request):
        return redirect("admin_login")

    error = ""

    if request.method == "POST":

        mn = request.POST.get("monument_name")
        ct = request.POST.get("category")
        city = request.POST.get("city")
        state = request.POST.get("state")
        gm = request.POST.get("google_map")
        sd = request.POST.get("short_description")
        dh = request.POST.get("detailed_history")
        ot = request.POST.get("opening_time")
        clt = request.POST.get("closing_time")
        bt = request.POST.get("best_time_to_visit")
        tt = request.POST.get("travel_tips")
        img = request.FILES.get("monument_image")
        adult_fee = request.POST.get("adult_fee") or 0
        child_fee = request.POST.get("child_fee") or 0
        foreign_fee = request.POST.get("foreign_fee") or 0

        # Featured checkbox
        is_featured = request.POST.get("is_featured") == "on"

        # Agar ye monument featured hai to pehle sabko unfeatured kar do
        if is_featured:
            Monument.objects.update(is_featured=False)

        Monument.objects.create(
            monument_name=mn,
            category=ct,
            city=city,
            state=state,
            google_map=gm,
            short_description=sd,
            detailed_history=dh,
            opening_time=ot,
            closing_time=clt,
            best_time_to_visit=bt,
            travel_tips=tt,
            monument_image=img,
            is_featured=is_featured,
            adult_fee=adult_fee,
            child_fee=child_fee,
            foreign_fee=foreign_fee,
        )

        error = "no"

    d = {"error": error}

    return render(request, "adminpanel/add_monument.html", d)


def view_monuments(request):
    if not check_admin(request):
        return redirect("admin_login")

    monuments = Monument.objects.all()
    
    d = {"monuments": monuments,}

    return render(request, "adminpanel/view_monuments.html", d)    


def delete_monument(request, pid):
    if not check_admin(request):
        return redirect("admin_login")

    monument = Monument.objects.get(id=pid)

    monument.delete()

    return redirect("view_monuments")    

def edit_monument(request, pid):
    if not check_admin(request):
        return redirect("admin_login")

    monument = Monument.objects.get(id=pid)

    if request.method == "POST":

        monument.monument_name = request.POST.get("monument_name")
        monument.category = request.POST.get("category")
        monument.city = request.POST.get("city")
        monument.state = request.POST.get("state")
        monument.google_map = request.POST.get("google_map")
        monument.short_description = request.POST.get("short_description")
        monument.detailed_history = request.POST.get("detailed_history")
        monument.opening_time = request.POST.get("opening_time")
        monument.closing_time = request.POST.get("closing_time")
        monument.best_time_to_visit = request.POST.get("best_time_to_visit")
        monument.travel_tips = request.POST.get("travel_tips")
        monument.adult_fee = request.POST.get("adult_fee") or 0
        monument.child_fee = request.POST.get("child_fee") or 0
        monument.foreign_fee = request.POST.get("foreign_fee") or 0

        # Featured checkbox
        is_featured = request.POST.get("is_featured") == "on"

        # Sirf ek hi featured monument rahe
        if is_featured:
            Monument.objects.update(is_featured=False)

        monument.is_featured = is_featured

        # Update image only if a new image is selected
        if request.FILES.get("monument_image"):
            monument.monument_image = request.FILES.get("monument_image")

        monument.save()

        return redirect("view_monuments")

    d = {
        "monument": monument,
    }

    return render(request, "adminpanel/edit_monument.html", d)


def add_gallery(request):
    if not check_admin(request):
        return redirect("admin_login")

    monuments = Monument.objects.all()

    if request.method == "POST":

        monument_id = request.POST.get("monument")
        caption = request.POST.get("caption")
        image = request.FILES.get("image")

        monument = Monument.objects.get(id=monument_id)

        Gallery.objects.create(
            monument=monument,
            caption=caption,
            image=image
        )

        return redirect("view_gallery")

    d = {
        "monuments": monuments,
    }

    return render(request, "adminpanel/add_gallery.html", d)

def view_gallery(request):
    if not check_admin(request):
        return redirect("admin_login")
    gallery = Gallery.objects.all()

    d = {
        "gallery": gallery,
    }

    return render(request, "adminpanel/view_gallery.html", d)


def delete_gallery(request, pid):
    if not check_admin(request):
       return redirect("admin_login")

    gallery = Gallery.objects.get(id=pid)
    gallery.delete()

    return redirect("view_gallery")    

def monument_details(request, pid):

    monument = get_object_or_404(Monument, id=pid)

    gallery = Gallery.objects.filter(monument=monument)

    d = {
        "monument": monument,
        "gallery": gallery,
    }

    return render(request, "monument_details.html", d)

@never_cache
def book_ticket(request, pid):

    if "user_email" not in request.session:
        return redirect("login")

    monument = get_object_or_404(Monument, id=pid)

    user = get_object_or_404(
        Register,
        email=request.session["user_email"]
    )

    if request.method == "POST":

        visit_date = request.POST.get("visit_date")

        adult_tickets = int(
            request.POST.get("adult_tickets") or 0
        )

        child_tickets = int(
            request.POST.get("child_tickets") or 0
        )

        if adult_tickets == 0 and child_tickets == 0:
            return render(
                request,
                "book_ticket.html",
                {
                    "monument": monument,
                    "error": "Please select at least one ticket."
                }
            )

        total_amount = (
            (Decimal(adult_tickets) * monument.adult_fee)
            +
            (Decimal(child_tickets) * monument.child_fee)
        )

        amount_in_paise = int(total_amount * 100)

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        razorpay_order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": f"booking_{user.id}_{monument.id}",
            "payment_capture": 1
        })

        booking = Booking.objects.create(
            user=user,
            monument=monument,
            visit_date=visit_date,
            adult_tickets=adult_tickets,
            child_tickets=child_tickets,
            total_amount=total_amount,
            payment_status="Pending",
            booking_status="Pending",
            razorpay_order_id=razorpay_order["id"]
        )

        return render(
            request,
            "booking_payment.html",
            {
                "booking": booking,
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                "razorpay_order_id": razorpay_order["id"],
                "amount": amount_in_paise,
                "user": user,
                "monument": monument,
            }
        )

    return render(
        request,
        "book_ticket.html",
        {
            "monument": monument
        }
    )

@never_cache
def payment_success(request):

    if "user_email" not in request.session:
        return redirect("login")

    booking_id = request.GET.get("booking_id")
    payment_id = request.GET.get("payment_id")
    signature = request.GET.get("signature")

    if not all([booking_id, payment_id, signature]):
        return render(request, "payment_failed.html", {
            "message": "Incomplete payment information."
        })

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user__email=request.session["user_email"]
    )

    # Use order ID stored in YOUR database
    order_id = booking.razorpay_order_id

    if not order_id:
        return render(request, "payment_failed.html", {
            "message": "Razorpay order ID is missing."
        })

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        })

    except razorpay.errors.SignatureVerificationError:
        return render(request, "payment_failed.html", {
            "message": "Payment verification failed."
        })

    # Payment verified successfully
    booking.razorpay_payment_id = payment_id
    booking.razorpay_signature = signature
    booking.payment_status = "Paid"
    booking.booking_status = "Confirmed"
    booking.save()
    try:
        send_mail(
            subject="Monument Ticket Booking Confirmation",
            message=f"""
    Dear {booking.user.fullname},

    Your monument ticket has been booked successfully.

    Booking ID: BK{booking.id}
    Monument: {booking.monument.monument_name}
    Visit Date: {booking.visit_date}
    Adult Tickets: {booking.adult_tickets}
    Child Tickets: {booking.child_tickets}
    Total Amount: ₹{booking.total_amount}

    Payment Status: Paid
    Booking Status: Confirmed

    Thank you for booking with Explore Bharat.
    """,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.user.email],
        fail_silently=False,
    )
    except Exception as e:
        print("EMAIL ERROR:", e)


    return render(request, "payment_success.html", {
        "booking": booking
    })


def contact_messages(request):
    if not check_admin(request):
         return redirect("admin_login")

    contacts = Contact.objects.all().order_by("-id")

    d = {
        "contacts": contacts
    }

    return render(request, "adminpanel/contact_messages.html", d)    

def delete_contact(request, pid):
    if not check_admin(request):
         return redirect("admin_login")

    contact = Contact.objects.get(id=pid)
    contact.delete()

    return redirect("contact_messages")    




def registered_users(request):
    if not check_admin(request):
         return redirect("admin_login")

    users = Register.objects.all().order_by("-id")

    d = {
        "users": users
    }

    return render(request, "adminpanel/registered_user.html", d)

def view_bookings(request):
    if not check_admin(request):
        return redirect("admin_login")

    bookings = Booking.objects.select_related(
        "user",
        "monument"
    ).order_by("-booking_date")

    return render(
        request,
        "adminpanel/view_bookings.html",
        {
            "bookings": bookings
        }
    )

def delete_user(request, pid):
    if not check_admin(request):
         return redirect("admin_login")

    user = Register.objects.get(id=pid)
    user.delete()

    return redirect("registered_users")


def check_admin(request):
    return request.session.get("admin", False)


def logout(request):

    request.session.flush()

    return redirect("admin_login")


def dashboard(request):

    if not check_admin(request):
         return redirect("admin_login")

    monument_count = Monument.objects.count()
    gallery_count = Gallery.objects.count()
    contact_count = Contact.objects.count()
    user_count = Register.objects.count()
    latest_monument = Monument.objects.order_by("-id").first()
    latest_user = Register.objects.order_by("-id").first()
    latest_contact = Contact.objects.order_by("-id").first()
    recent_monuments = Monument.objects.order_by("-id")[:5]
    d = {
    "monument_count": monument_count,
    "gallery_count": gallery_count,
    "contact_count": contact_count,
    "user_count": user_count,

    "latest_monument": latest_monument,
    "latest_user": latest_user,
    "latest_contact": latest_contact,
    "recent_monuments": recent_monuments,
    }

    return render(request, "adminpanel/dashboard.html", d)


def admin_login(request):

    error=""

    if request.method=="POST":

        email=request.POST["email"]
        password=request.POST["password"]

        if email=="admin@gmail.com" and password=="admin123":

            request.session["admin"]=True

            error="no"

        else:

            error="yes"

    d={"error":error}

    return render(request,"adminpanel/admin_login.html",d)    

