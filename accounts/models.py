import re
from datetime import datetime as dt

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.core import validators
from django.db import models

from accounts import constants


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        "Apelido / Usuário",
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile(r"^[\w.@+-]+$"),
                "Informe um nome de usuário válido. "
                "Este valor deve conter apenas letras, números "
                "e os caracteres: @/./+/-/_ .",
                "invalid",
            )
        ],
        help_text="Um nome curto que será usado para identificá-lo de forma única na plataforma",
    )
    name = models.CharField("Nome", max_length=100, blank=True)
    email = models.EmailField("E-mail", unique=True)
    is_staff = models.BooleanField("Equipe", default=False)
    is_active = models.BooleanField("Ativo", default=True)
    date_joined = models.DateTimeField("Data de Entrada", auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.name or self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(" ")[0]


class BaseManager(models.Manager):
    """
    Base Manager for Base model
    """

    def __init__(self):
        super(BaseManager, self).__init__()

    # If you are using newer versions of Django you will need to define this
    # def get_queryset(self):
    #     return super(BaseManager, self).get_queryset().filter(deleted=True)


class Base(models.Model):
    """
    Base parent model for all the models
    """

    created_at = models.DateTimeField("Criado em", auto_now_add=True, null=True)
    modified_at = models.DateTimeField("Atualizado em", auto_now=True, null=True)
    status = models.BooleanField(choices=constants.STATUS, default=constants.ATIVO)

    objects = BaseManager()

    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True

    # Override save method.
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = dt.now()

        modified_at = kwargs.pop("update_timestamp", False)
        if modified_at:
            self.modified_at = dt.now()

        super(Base, self).save(*args, **kwargs)
