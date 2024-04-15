from django.db import models

# Create your models here.




class post(models.models):
    POST_TYPE_CHOICES = [
        ('music', 'music'),
        ('show', 'show'),
        ('cinema','cinema'),
        
    ]



    b_name = models.CharField(max_length=50)
    b_text = models.TextField()
    b_type = models.CharField(choices=POST_TYPE_CHOICES)
    b_image = models.ImageField(upload_to = 'blog/' , null = True , blank = True)
    


