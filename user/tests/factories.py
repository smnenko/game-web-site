import factory
import django.contrib.auth.models as auth
from django.utils.timezone import now


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'user.CustomUser'
        django_get_or_create = ('username', 'email', 'first_name', 'last_name', 'password', 'birth_date')

    username = 'custom'
    password = 'custompasswd'
    email = 'custom@gmail.com'
    first_name = 'Custom'
    last_name = 'User'
    birth_date = now()

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for group in extracted:
                self.groups.add(group)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.Group'
        django_get_or_create = ('name', )

    name = 'user'
