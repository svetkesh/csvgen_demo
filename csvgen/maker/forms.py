from django import forms
from .models import Schema, Column


class SchemaForm(forms.ModelForm):

    class Meta:
        model = Schema
        fields = [
            'name', 'column_separator', 'column_separator',
            'string_character',
        ]


class ColumnForm(forms.ModelForm):

    class Meta:
        model = Column
        fields = (
            'name', 'type',
            'start', 'end',
            'order',
        )
