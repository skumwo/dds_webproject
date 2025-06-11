from django import forms
from .models import CashFlowRecord, Category, SubCategory, Status, Type

class CashFlowRecordForm(forms.ModelForm):
    class Meta:
        model = CashFlowRecord
        fields = [
            'custom_date', 'status', 'type',
            'category', 'subcategory', 'amount', 'comment'
        ]
        widgets = {
            'custom_date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['subcategory'].queryset = SubCategory.objects.all()

        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif getattr(self.instance, 'type_id', None):
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)

        # Если выбрана категория (например, после отправки формы)
        if 'category' in self.data:
            try:
                cat_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=cat_id)
            except (ValueError, TypeError):
                pass
        elif getattr(self.instance, 'category_id', None):
            self.fields['subcategory'].queryset = SubCategory.objects.filter(category=self.instance.category)


