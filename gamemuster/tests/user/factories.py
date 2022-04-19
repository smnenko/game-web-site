import factory
from django.utils.timezone import now


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'user.CustomUser'
        django_get_or_create = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'birth_date'
        )

    password = 'custompassword'
    email = 'custom@gmail.com'
    first_name = 'Custom'
    last_name = 'User'
    birth_date = now()

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.groups.set(extracted)


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'auth.Group'
        django_get_or_create = ('name', )

    name = 'user'
