from django.db import models

# Create your models here.




class Blog(models.Model):
    BlogTitle = models.CharField(max_length=50)
    BlogDescription = models.TextField()
    BlogType = models.CharField(max_length=50)
    BlogImage = models.ImageField(upload_to='blog/', null=True, blank=True)
    SeoTitle = models.CharField(max_length=50, blank=True, null=True)
    SeoDescription = models.CharField(max_length=50, blank=True, null=True)
    SeoKeywords = models.CharField(max_length=50, blank=True, null=True)
    SeoIndexpage = models.BooleanField(default=False, blank=True, null=True)
    SeoCanonical = models.URLField(max_length=200, blank=True, null=True)
    SeoSchema = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.BlogTitle

    @classmethod
    def add_BlogType_choice(cls, choice):
        field = cls._meta.get_field('BlogType')
        current_choices = list(field.choices) if field.choices else []
        if choice not in current_choices:
            current_choices.append((choice, choice))
            field.choices = current_choices

