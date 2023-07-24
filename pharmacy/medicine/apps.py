from django.apps import AppConfig


class MedicineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medicine'
    verbose_name= 'محصول'
    verbose_name_plural='محصولات'
