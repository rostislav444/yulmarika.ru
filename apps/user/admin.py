from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from apps.user.models import CustomUser, UserAdress



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields =  (
            'email',
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.password = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user
   


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'gender',
            'name',
            'surname',
            'phone',
            'email',
            'date_of_birth',
            'password',
            'city',
            'street',
            'house',
            'appartment',
            'index',
            'add_info',
            'updated',
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        if self.instance.is_admin:
            return self.initial["password"]
        return self.data["password"]
        

class UserAdressInline(admin.StackedInline):
    model = UserAdress
    extra = 0


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = (UserAdressInline,)

    def get_adress(self, user=None):
        if user:
            fields = ['city','index','street','house','appartment']
            adress_data = []
            for field in fields:
                attr = getattr(user, field)
                if attr:
                    adress_data.append(str(attr))
                else:
                    return ""
            adress = "Россия, " + ", ".join(adress_data)
            return adress
        return ""
    get_adress.short_description = 'Адрес'

    readonly_fields = ('updated','get_adress',)
    list_display = ('id','name','gender','phone','email','get_adress','created')

    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': (
            'user_id',
            'gender',
            'name',
            'surname',
            'phone',
            'email',
            'date_of_birth',
            'password',
            'city',
            'street',
            'house',
            'appartment',
            'index',
            'add_info',
            'updated',
        )}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
        
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            
            'fields' : (
                'gender',
                'name',
                'surname',
                'phone',
                'email',
                'date_of_birth',
                'password1',
                'password2',
                'city',
                'street',
                'house',
                'appartment',
                'index',
                'add_info',
                'updated',
            )
        }),
    )
    
    search_fields = ('id','name','gender','phone','email','city','street')
    ordering = ('-created',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)