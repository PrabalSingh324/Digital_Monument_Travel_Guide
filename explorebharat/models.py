from django.db import models

# Create your models here.
class Contact(models.Model):
    full_name = models.CharField(max_length=100,null=True)
    email = models.CharField(max_length=100,null=True)
    subject = models.CharField(max_length=200,null=True)
    message = models.CharField(max_length=200,null=True)
    
    
class Register(models.Model):
    fullname=models.CharField(max_length=100, null=True)
    username=models.CharField(max_length=100, null=True)
    email=models.CharField(max_length=100, null=True)
    phone=models.CharField(max_length=15, null=True)
    password=models.CharField(max_length=100, null=True)
    confirm_password=models.CharField(max_length=100, null=True)
    gender=models.CharField(max_length=20, null=True)


class Monument(models.Model):

    monument_name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)

    google_map = models.CharField(max_length=500, null=True)

    short_description = models.CharField(max_length=300, null=True)
    detailed_history = models.TextField(null=True)

    opening_time = models.CharField(max_length=50, null=True)
    closing_time = models.CharField(max_length=50, null=True)

    best_time_to_visit = models.CharField(max_length=300, null=True)

    travel_tips = models.TextField(null=True)

    monument_image = models.ImageField(upload_to="monuments/", null=True)
    adult_fee = models.DecimalField(
    max_digits=8,
    decimal_places=2,
    default=0
    )

    child_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    foreign_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )


    #featured monument
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.monument_name
   


class Gallery(models.Model):
    monument = models.ForeignKey(Monument, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.monument.monument_name

class Booking(models.Model):

    user = models.ForeignKey(
        Register,
        on_delete=models.CASCADE
    )

    monument = models.ForeignKey(
        Monument,
        on_delete=models.CASCADE
    )

    visit_date = models.DateField()

    adult_tickets = models.PositiveIntegerField(default=0)

    child_tickets = models.PositiveIntegerField(default=0)

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_status = models.CharField(
        max_length=20,
        default="Pending"
    )

    booking_status = models.CharField(
        max_length=20,
        default="Confirmed"
    )

    booking_date = models.DateTimeField(
        auto_now_add=True
    )
    razorpay_order_id = models.CharField(
    max_length=100,
    blank=True,
    null=True
    )
    
    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    
    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    def __str__(self):
        return f"Booking #{self.id} - {self.monument.monument_name}"        