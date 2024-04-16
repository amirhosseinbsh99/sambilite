from django.db import models

# Create your models here.




class post(models.models):
    POST_TYPE_CHOICES = [
        ('music', 'music'),
        ('show', 'show'),
        ('cinema','cinema')
    ]

    b_name = models.CharField(max_length=50)
    b_text = models.TextField()
    b_type = models.CharField(choices=POST_TYPE_CHOICES)
    b_image = models.ImageField(upload_to = 'blog/' , null = True , blank = True)
    SeoTitle =  models.CharField(max_length=50)
    SeoDescription=  models.CharField(max_length=50)
    SeoKeywords= models.CharField(max_length=50)
    SeoIndexpage = models.BooleanField(default=False)
    SeoCanonical= models.models.URLField( max_length=200)
    SeoSchema=models.models.URLField( max_length=200)

    


