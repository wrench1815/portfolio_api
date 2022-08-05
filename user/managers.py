from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations: True

    def _create_user(self, username, password, **kwargs):
        '''
            Creates and saves a User with given Username, Password and Additional fields.
        '''
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def createuser(self, username, password, **kwargs):
        kwargs.setdefault('is_superuser', False)

        return self._create_user(username, password, **kwargs)

    def _create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(username, password, **kwargs)
