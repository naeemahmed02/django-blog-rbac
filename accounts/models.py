from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from froala_editor.fields import FroalaField


class MyAccountManager(BaseUserManager):
    
    # Methods to create active and superuser
    
    def create_user(self, first_name, last_name, email, username, phone_number = None, password = None):
        
        if not email:
            raise ValueError("User must have an email address")
        
        if not username:
            raise ValueError("User must have a username")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            phone_number = phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password):
        
        user = self.create_user(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        # user.is_super_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=40, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # System Flags
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_super_user = models.BooleanField(default=False)
    
    objects = MyAccountManager()
    
    # set username as email
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    bio = FroalaField()
    profile_pic = models.ImageField(
        verbose_name="Profile Picture", 
        upload_to='user_profiles', 
        default='user_profiles/default.png')
    whatsapp_number = models.CharField(max_length=20, null= True, blank=True)
    
    
    def __str__(self):
        return str(self.user.get_full_name)
    