from django import forms

from pursuer.models import Man


class ManForm(forms.ModelForm):
    class Meta:
        model = Man
        fields = ['name']

    persecuted = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Man.objects.all())
    pursued = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Man.objects.all())

    def __init__(self,  *args, **kwargs):
        super(ManForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            if instance.follow_ids:
                self.fields['persecuted'].initial = Man.objects.filter(id__in=instance.follow_ids.split(' '))
            else:
                self.fields['persecuted'].initial = Man.objects.none()

            self.fields['pursued'].initial = Man.objects.filter(follow_ids__contains=instance.id)

    def save(self, commit=True):
        instance = super(ManForm, self).save(commit=False)

        if 'persecuted' in self.changed_data:
            persecuted = self.cleaned_data.get('persecuted')

            instance.follow_ids = ' '.join((str(p.id) for p in persecuted))

        if 'pursued' in self.changed_data:
            pursued = self.cleaned_data.get('pursued')
            current_pursued = Man.objects.filter(follow_ids__contains=instance.id)

            excluded = current_pursued.exclude(pk__in=pursued)
            for e in excluded:
                new_ids = [str(i) for i in e.follow_ids.split(' ') if i != str(instance.id)]
                if new_ids:
                    e.follow_ids = ' '.join(new_ids)
                else:
                    e.follow_ids = ''
                e.save()

            added = pursued.exclude(pk__in=current_pursued)
            for a in added:
                if a.follow_ids:
                    a.follow_ids = ' '.join(a.follow_ids.split(' ') + [str(instance.id)])
                else:
                    a.follow_ids = str(instance.id)
                a.save()

        if commit:
            instance.save()
        return instance
