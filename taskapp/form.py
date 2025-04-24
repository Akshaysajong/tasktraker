from django import forms
from .models import Task, UserProfile, User
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
 
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']

    

class UserCreateForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    role = forms.ChoiceField(
        choices=UserProfile.USER_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
    )

   

    class Meta:
        model = User
        fields = ['username', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        # Exclude SuperAdmin from role choices
        self.fields['role'].choices = [
            (key, label) for key, label in UserProfile.USER_TYPES if key != 'superadmin'
        ]

    def save(self, commit=True):
        user = super().save(commit)
        role = self.cleaned_data.get('role')
        UserProfile.objects.create(user=user, user_type=role)
        return user


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    user_type = forms.ChoiceField(
        choices=UserProfile.USER_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    assigned_admin = forms.ModelChoiceField(
        queryset=User.objects.filter(userprofile__user_type='admin'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('instance', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        if self.user_instance:
            self.fields['username'].initial = self.user_instance.username
            self.fields['email'].initial = self.user_instance.email
            try:
                profile = self.user_instance.userprofile
                self.fields['user_type'].initial = profile.user_type
                if profile.user_type == 'user':
                    self.fields['assigned_admin'].initial = profile.assigned_admin
                else:
                    self.fields.pop('assigned_admin', None)
            except UserProfile.DoesNotExist:
                self.fields.pop('assigned_admin', None)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        print(f"Cleaning username: {username}")

        if username:
            if username != self.user_instance.username:
                qs = User.objects.filter(username=username)

                if self.user_instance and self.user_instance.id:
                    qs = qs.exclude(id=self.user_instance.id)

                if qs.exists():
                    print(f"Error: User with username {username} already exists.")
                    raise forms.ValidationError("A user with that username already exists.")
        
        return username
    
    def save(self, commit=True):
        
        user = self.user_instance
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']

        if username != user.username:
            user.username = username

        if email != user.email:
            user.email = email
            print('user', user)

        if commit:
            user.save()

            # Update the profile information
            profile = user.userprofile
            profile.user_type = self.cleaned_data['user_type']
            
            if profile.user_type == 'user':
                profile.assigned_admin = self.cleaned_data.get('assigned_admin')
            else:
                profile.assigned_admin = None

            profile.save()
        
        return user


class TaskUpdateForm(forms.ModelForm):
    title = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(userprofile__user_type='user'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=Task.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'status']
        


