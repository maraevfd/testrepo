from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Cost(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    amount = models.IntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "Расходы в количестве {} руб. потрачено на категорию {}"\
            .format(self.title, self.category.name)
