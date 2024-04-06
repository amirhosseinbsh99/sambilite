from django.db import models


class Concert(models.Model):
    CONCERT_STATUS_CHOICES = [
        ('Soldout', 'Soldout'),
        ('active', 'active')
    ]
    CONCERT_TYPE_CHOICES = [
        ('music', 'music'),
        ('show', 'show')
    ]

    co_id = models.AutoField(primary_key=True)
    co_name = models.CharField(max_length=250)
    co_type = models.CharField(max_length=250,choices=CONCERT_TYPE_CHOICES,default='music')
    co_date = models.DateTimeField(max_length=250)
    co_address = models.CharField(max_length=250, blank=True)
    co_seats = models.IntegerField(blank=True)
    co_image = models.ImageField(upload_to = 'blog/' , null = True , blank = True)
    a_name = models.CharField(max_length=250)
    co_status = models.CharField(max_length=20, choices=CONCERT_STATUS_CHOICES, default='active')

    

class Customer(models.Model):
    cu_id = models.AutoField(primary_key=True)
    cu_name = models.CharField(max_length=250)
    cu_phonenumber = models.CharField(max_length=250, blank=True)
    cu_email = models.EmailField(max_length=250)
    def __str__(self) -> str:
        return f"cu_id: {self.cu_id},cu_phonenumber: {self.cu_phonenumber}"

class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ('Empty', 'Empty'),
        ('Reserved', 'Reserved'),
        ('Reserving', 'Reserving')
    
    ]
    se_id = models.AutoField(primary_key=True)
    se_area = models.CharField(max_length=250, blank=True)
    se_row = models.IntegerField(blank=True)
    se_number = models.IntegerField(blank=True)
    se_status = models.CharField(max_length=20, choices=SEAT_STATUS_CHOICES, default='Empty')
    se_price = models.DecimalField(max_digits=10, decimal_places=2)

class Sans(models.Model):
    sa_id = models.AutoField(primary_key=True)
    sa_number = models.IntegerField(blank=True)
    sa_time = models.TimeField(blank=False)
    co_id = models.ForeignKey(Concert, on_delete=models.CASCADE)




class Ticket(models.Model):
    t_id = models.AutoField(primary_key=True)
    sa_id = models.ForeignKey(Sans, on_delete=models.CASCADE)
    se_id = models.ForeignKey(Seat, on_delete=models.CASCADE)
    co_id = models.ForeignKey(Concert, on_delete=models.CASCADE)



class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    
    ]

    payment_id = models.AutoField(primary_key=True)
    t_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    se_id = models.ForeignKey(Seat, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Payment ID: {self.payment_id}, Ticket ID: {self.ticket_id}, Amount: {self.payment_amount}, Status: {self.payment_status}"