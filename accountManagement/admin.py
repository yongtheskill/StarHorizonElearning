from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms

from .models import User, Course, StudentClass, Module


from django.contrib.auth.models import Group

admin.site.unregister(Group)



# Register your models here.


class CourseAdmin(admin.ModelAdmin):

    readonly_fields = ('id', )

    fieldsets = (
        (None, {'fields': ('courseName',)}),
        ('Details', {'fields': ('courseInstitution', 'courseDescription', 'quizTags', 'id')}),
    )

    def __str__(self):
        return self.courseName

class StudentClassAdmin(admin.ModelAdmin):

    readonly_fields = ('id', )

    fieldsets = (
        (None, {'fields': ('className',)}),
        ('Details', {'fields':('classInstitution', 'courses', 'id')}),
    )

    def __str__(self):
        return self.className

class ModuleAdmin(admin.ModelAdmin):

    readonly_fields = ('id', )

    fieldsets = (
        (None, {'fields': ('moduleName',)}),
        ('Details', {'fields':('course', 'id', )}),
    )

    def __str__(self):
        return self.moduleName

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    list_filter = ("accountType", )
    add_form = UserCreationForm
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phoneNumber', 'accountType', 'institution', 'profilePic', )}),
        ('Course info', {'fields': ('classes', )}),
        ('Quiz Responses', {'fields': ('quizResponses', )}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),
        #('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phoneNumber', 'first_name', 'last_name', 'accountType', 'institution', 'classes',)}
        ),
    )
    
    def __str__(self):
        return self.username    


admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(StudentClass, StudentClassAdmin)
admin.site.register(Module, ModuleAdmin)