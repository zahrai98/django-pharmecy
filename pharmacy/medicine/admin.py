from django.contrib import admin
from .models import Category,Product,Brand,Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields =  {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','available','count')
    list_filter = ('available','expiration_date','date_of_manufacture')
    list_editable = ('price','count','available')
    prepopulated_fields = {'slug':('name',)}
    raw_id_fields = ('category',)
    actions = ('make_available',)

    def make_available(self,request,queryset):
        raws=queryset.update(available=True)
        self.message_user(request,f'{raws} updated')
    make_available.short_description = 'make all available'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields =  {'slug':('name',)}

admin.site.register(Comment)
