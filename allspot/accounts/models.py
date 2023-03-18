# Import necessary modules
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import OneToOneField

# Define a custom user manager
class UserManager(BaseUserManager):
    # Define a method to create a new user
    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        # Ensure that the user has an email address
        if not email:
            raise ValueError('O utilizador tem que ter email.')
        
        # Ensure that the user has a username
        if not username:
            raise ValueError('O utilizador tem que ter um nome de utilizador.')
        
        # Create a new user object with the given parameters
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )
        # Set the user's password and save the user to the database
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Define a method to create a new superuser
    def create_superuser(self, first_name, last_name, username, email, password=None):
        # Create a new user with the given parameters
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        # Set the user's admin status and other permissions and save to database
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user

# create a custom user model that extends AbstractBaseUser
class User(AbstractBaseUser):
    # define constants to be used for user roles
    VENDOR = 1
    CUSTOMER = 2
    
    # create a tuple of choices for user roles
    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Utilizador'),
    )
    
    # define user model fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=9, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    # define model fields for tracking user activity
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # define the field to be used as the username field when authenticating users
    USERNAME_FIELD = 'email'
    # define the required fields when creating a user
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    # specify the custom user manager to be used with this model
    objects = UserManager()

    # define a method to return the user's email address
    def __str__(self):
        return self.email
    
    # define a method to determine if the user has a specific permission
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    # define a method to determine if the user has permissions to access a specific app
    def has_module_perms(self, app_label):
        return True
    
    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    address_line_1 = models.CharField(max_length=50, blank=True, null=True)
    address_line_2 = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=25, blank=True, null=True)
    district = models.CharField(max_length=25, blank=True, null=True)
    concelho = models.CharField(max_length=25, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.CharField(max_length=25, blank=True, null=True)
    longitude = models.CharField(max_length=25, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

