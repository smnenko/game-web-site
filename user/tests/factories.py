import factory


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'user.CustomUser'
        django_get_or_create = ('username', 'email', 'first_name', 'last_name', 'password')

    username = 'custom'
    password = 'custompasswd'
    email = 'custom@gmail.com'
    first_name = 'Custom'
    last_name = 'User'
