from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Schema(models.Model):
    COMMA = ','
    SEMICOLON = ';'
    DOUBLE_QUOT = '"'
    SINGLE_QUOT = "'"

    COLUMN_SEPARATORS = [
        (COMMA, 'Comma (,)'),
        (SEMICOLON, 'Semicolon (;)'),
    ]
    STRING_SEPARATORS = [
        (SINGLE_QUOT, "Quotation mark (')"),
        (DOUBLE_QUOT, 'Double quotation mark (")'),
    ]

    name = models.CharField(
        max_length=40,
    )

    column_separator = models.CharField(
        max_length=1,
        choices=COLUMN_SEPARATORS,
        default=COMMA,
    )

    string_character = models.CharField(
        max_length=1,
        choices=STRING_SEPARATORS,
        default=DOUBLE_QUOT
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    modified = models.DateField(
        auto_now=True
    )

    def get_absolute_url(self):
        return reverse("schema_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.name} from {self.modified}'

    def schema_update(self):
        self.modified = timezone.now()
        self.save()


class Column(models.Model):

    FULL_NAME = 'Full name'
    INTEGER = 'Integer'
    COMPANY = 'Company'
    JOB = 'Job'
    DOMAIN = 'Domain'

    TYPE_CHOICES = [
        (FULL_NAME, 'Full name'),
        (INTEGER, 'Integer'),
        (COMPANY, 'Company'),
        (JOB, 'Job'),
        (DOMAIN, 'Domain'),
    ]

    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)

    name = models.CharField(
        max_length=40,
    )

    type = models.CharField(
        max_length=40,
        choices=TYPE_CHOICES,
    )

    start = models.IntegerField(
        blank=True,
        null=True,
    )

    end = models.IntegerField(
        blank=True,
        null=True,
    )

    order = models.SmallIntegerField()

    class Meta:
        unique_together = ['schema', 'order']
        ordering = ['order']

    def get_absolute_url(self):
        return reverse("schema_list")

    def __str__(self):
        return f'{self.name} of {self.type} type'
