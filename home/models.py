from django.db import models
from accounts.models import Customer


class Concert(models.Model):
    CONCERT_STATUS_CHOICES = [
        ('soldout', 'Soldout'),
        ('active', 'Active'),
        ('comingsoon', 'ComingSoon')
    ]
    CONCERT_TYPE_CHOICES = [
        ('music', 'Music'),
        ('show', 'Show'),
        ('cinema', 'Cinema')
    ]

    concert_name = models.CharField(max_length=100)
    concert_type = models.CharField(max_length=10, choices=CONCERT_TYPE_CHOICES, default='music')
    concert_date = models.DateField()
    concert_address = models.CharField(max_length=250, blank=True)
    concert_image = models.ImageField(upload_to='blog/', null=True, blank=True)
    concert_location = models.CharField(max_length=40)
    artist_name = models.CharField(max_length=100)
    concert_status = models.CharField(max_length=20, choices=CONCERT_STATUS_CHOICES, default='active')
    number_of_rows = models.IntegerField()
    number_of_sans = models.IntegerField()

    def __str__(self):
        return f"concert: {self.concert} - {self.concert_name}"


class Slider(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='sliders/', null=True, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return f"concert: {self.concert} - {self.title}"


class Sans(models.Model):
    SANS_STATUS = [
        ('active', 'Active'),
        ('soldout', 'Soldout'),
    ]

    sans_number = models.IntegerField(blank=True)
    sans_status = models.CharField(max_length=20, choices=SANS_STATUS, default='active')
    sans_time = models.TimeField(null=True, blank=True)
    sans_date = models.DateField(null=True, blank=True)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)

    def __str__(self):
        return f"sans_id: {self.sans_id} - sans_number: {self.sans_number} - {self.concert.concert_name} - sans_status: {self.sans_status}"


class Rows(models.Model):
    ROW_AREA_CHOICES = [
        ('vip', 'VIP'),
        ('balcony', 'Balcony'),
        ('ground', 'Ground')
    ]

    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    row_number = models.IntegerField()
    row_price = models.IntegerField(null=True, blank=True)
    row_area = models.CharField(max_length=7, choices=ROW_AREA_CHOICES, default='ground')
    number_of_seat = models.IntegerField(blank=True, null=True)
    sans = models.ForeignKey(Sans, related_name='rows', on_delete=models.CASCADE)

    def __str__(self):
        return f"row_number: {self.row_number} - {self.concert.concert_name}"


class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ('empty', 'Empty'),
        ('reserved', 'Reserved'),
        ('reserving', 'Reserving'),
        ('not_buyable', 'Not Buyable'),
        ('selected', 'Selected'),
        ('space', 'Space')
    ]

    concert = models.ForeignKey(Concert, related_name='seats', on_delete=models.CASCADE)
    row = models.ForeignKey(Rows, related_name='rows_number', on_delete=models.CASCADE)
    seat_number = models.IntegerField(blank=True, null=True)
    seat_status = models.CharField(max_length=20, choices=SEAT_STATUS_CHOICES, default='empty')
    seat_price = models.IntegerField(null=True, blank=True)

    def select_seat(self):
        if self.seat_status == 'empty':
            self.seat_status = 'selected'
            self.save()
            return True
        return False

class Order(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=9, choices=PAYMENT_STATUS_CHOICES)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    authority = models.CharField(max_length=50, blank=True, null=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    concert = models.OneToOneField(Concert, on_delete=models.CASCADE)