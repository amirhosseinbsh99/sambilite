from django.db import models
from accounts.models import Customer


class Concert(models.Model):
    CONCERT_STATUS_CHOICES = [
        ('Soldout', 'Soldout'),
        ('Active', 'Active'),
        ('ComingSoon','ComingSoon')
    ]
    CONCERT_TYPE_CHOICES = [
        ('music', 'music'),
        ('show', 'show'),
        ('cinema','cinema')
    ]

    ConcertId = models.AutoField(primary_key=True)
    ConcertName = models.CharField(max_length=100)
    ConcertType = models.CharField(max_length=10,choices=CONCERT_TYPE_CHOICES,default='music')
    ConcertDate = models.DateTimeField(max_length=20)
    ConcertAddress = models.CharField(max_length=250, blank=True)
    ConcertImage = models.ImageField(upload_to = 'blog/' , null = True , blank = True)
    ConcertLocation = models.CharField(max_length=40)
    ArtistName = models.CharField(max_length=100)
    ConcertStatus = models.CharField(max_length=20, choices=CONCERT_STATUS_CHOICES, default='ComingSoon')
    NumberofRows = models.IntegerField() 
    NumberofSans = models.IntegerField() 


    def __str__(self):
        return f"{'concertid: ',self.ConcertId} - {self.ConcertName}"
    
    
class Sans(models.Model):
    SansId = models.AutoField(primary_key=True)
    SansNumber = models.IntegerField(blank=True)
    SansTime = models.TimeField(blank=False)
    ConcertId = models.ForeignKey(Concert, on_delete=models.CASCADE)
    
  

class Rows(models.Model):
    Row_Area_CHOICES = [
        ('VIP', 'VIP'),
        ('balcony', 'balcony'),
        ('ground', 'ground')

    ]

    ConcertId = models.ForeignKey(Concert, on_delete=models.CASCADE)
    Rowid = models.AutoField(primary_key=True)
    RowNumber = models.IntegerField()
    RowPrice =  models.IntegerField(null=True,blank=True) 
    RowArea = models.CharField(max_length=7, choices=Row_Area_CHOICES, blank=True)
    NumberofSeat = models.IntegerField(blank=True,null=True)
    SansId = models.ForeignKey(Sans, related_name='rows', on_delete=models.CASCADE)
    def __str__(self):
        return f"{'rowid: ',self.Rowid,'rowNumber: ',self.RowNumber} - {self.ConcertId.ConcertName} - {self.Rowid}"
    

class Seat(models.Model):
    SEAT_STATUS_CHOICES = [
        ('Empty', 'Empty'),
        ('Reserved', 'Reserved'),
        ('Reserving', 'Reserving'),
        ('not_buyable','not_buyable'),
        ('selected','selected'),
        ('space','space')
    ]
    
    ConcertId = models.ForeignKey(Concert,related_name='Concert_name', on_delete=models.CASCADE)
    Rowid = models.ForeignKey(Rows,related_name='Rows_Number', on_delete=models.CASCADE)
    SeatId = models.AutoField(primary_key=True)
    SeatNumber = models.IntegerField(blank=True,null=True)
    SeatStatus = models.CharField(max_length=20, choices=SEAT_STATUS_CHOICES, default='Empty')
    SeatPrice = models.IntegerField(null=True,blank=True) 
    
   





class Ticket(models.Model):
    TicketId = models.AutoField(primary_key=True)
    Ticket_Serial = models.CharField(max_length=15)
    SansId = models.OneToOneField(Sans, on_delete=models.CASCADE)
    SeatId = models.OneToOneField(Seat, on_delete=models.CASCADE)
    ConcertId = models.OneToOneField(Concert, on_delete=models.CASCADE)



class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('canceled','canceled')
    
    ]

    PaymentId = models.AutoField(primary_key=True)
    TicketId = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    SeatId = models.ForeignKey(Seat, on_delete=models.CASCADE)
    PaymentDate = models.DateTimeField(auto_now_add=True)
    PaymentStatus = models.CharField(max_length=9, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    CustomerId = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # def __str__(self):
    #     return f"Payment ID: {self.payment_id}, Ticket ID: {self.ticket_id}, Amount: {self.payment_amount}, Status: {self.payment_status}"    
    #total price of the seats
    # @property
    # def total_price(self):
    #     total = [for seat in seats]

    