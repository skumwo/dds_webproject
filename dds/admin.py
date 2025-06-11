from django.contrib import admin
from .models import Status, Type, Category, SubCategory, CashFlowRecord

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    inlines = [SubCategoryInline]

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

class CashFlowRecordAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'custom_date', 'status', 'type', 'category', 'subcategory', 'amount')
    list_filter = ('status', 'type', 'category', 'subcategory', 'created_at')
    search_fields = ('comment',)

admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(CashFlowRecord, CashFlowRecordAdmin)
