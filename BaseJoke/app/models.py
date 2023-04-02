from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.CharField(max_length=200)
    author = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='quotes')

    def __str__(self):
        return f"{self.text} - {self.author}"

