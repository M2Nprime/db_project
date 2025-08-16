from django.contrib import admin
from .models import Movie, Person, Genre

# کلاس ادمین برای شخصی‌سازی نمایش مدل Person
class PersonAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'birthdate', 'nationality', 'age') # پراپرتی 'age' را هم اضافه کردیم
    search_fields = ('fullname',)

# کلاس ادمین برای شخصی‌سازی نمایش مدل Movie با استفاده از fieldsets
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'releaseyear', 'country', 'tmdbscore', 'directorid', 'get_duration_display')
    list_filter = ('releaseyear', 'country')
    search_fields = ('title', 'summary')
    
    # گروه‌بندی فیلدها در صفحه ویرایش
    fieldsets = (
        ('اطلاعات اصلی فیلم', {
            'fields': ('title', 'summary', 'posterurl')
        }),
        ('جزئیات انتشار و امتیاز', {
            'fields': ('releaseyear', 'tmdbscore', 'durationinminutes', 'country')
        }),
        ('عوامل فیلم', {
            'fields': ('directorid',),
            'classes': ('collapse',)  # این بخش را به صورت جمع‌شونده نمایش می‌دهد
        }),
    )

# ثبت کردن مدل‌ها در پنل ادمین
admin.site.register(Movie, MovieAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Genre)