from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where phone_number is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a regular User with the given phone number and password.
        """
        if not phone_number:
            raise ValueError('The Phone Number field must be set')

        # Create a new User instance with the provided phone_number and extra_fields
        user = self.model(phone_number=phone_number, **extra_fields)

        # Set the password, which automatically handles hashing
        # If no password is provided, set_password(None) will clear it,
        # which aligns with your model's null=True, blank=True for password.
        # However, for login purposes, a password will be required.
        user.set_password(password)

        # Save the user to the database
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a Superuser with the given phone number and password.
        Superusers are automatically made staff and active.
        """
        # Ensure that is_staff, is_superuser, and is_active are set to True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Superusers should always be active

        # Validate that the superuser fields are correctly set
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Call the create_user method to create the superuser
        return self.create_user(phone_number, password, **extra_fields)
