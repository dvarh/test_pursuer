from django.contrib import admin

from pursuer.forms import ManForm
from pursuer.models import Man


class ManAdmin(admin.ModelAdmin):
    form = ManForm

    list_display = ('name', 'persecuted_count', 'pursued_count')

    fieldsets = (
        (None, {
            'fields': ('name', 'persecuted', 'pursued'),
        }),
    )

    def persecuted_count(self, instance):
        if instance.follow_ids == '':
            return 0
        return Man.objects.filter(id__in=instance.follow_ids.split(' ')).count()

    persecuted_count.short_description = 'Count persecuted Man\'s'

    def pursued_count(self, instance):
        return Man.objects.filter(follow_ids__contains=instance.id).count()

    pursued_count.short_description = 'Count pursued Man\'s'


admin.site.register(Man, ManAdmin)
