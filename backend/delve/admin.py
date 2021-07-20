from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import Drug, Combo
from .models import Drug, Scientists, Combo, Ic50, Cellline, Cancer, Profile, ML_Result
class ProfileAdmin(UserAdmin):
    list_display = ('email', 'last_name', 'first_name', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_field = ('email', 'last_name', 'first_name')
    readonly_fields = ('date_joined', 'last_login', 'authy_id')

    filter_horizontal = ()
    # list_fiter = ('email', 'last_name', 'first_name', 'is_admin', 'is_staff')
    fieldsets = ()
    ordering = ('email',)

class M2MAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'ML'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)
        
# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Drug)
admin.site.register(Cellline)
admin.site.register(Cancer)
admin.site.register(Scientists)
admin.site.register(Combo)
admin.site.register(Ic50)
admin.site.register(ML_Result)
# admin.site.register(Models, M2MAdmin)



# from django.contrib.admin import AdminSite
# class MyAdminSite(AdminSite):
#     site_header = 'Monty Python administration'

# admin_site = MyAdminSite(name='myadmin')
# admin_site.register(MyModel)