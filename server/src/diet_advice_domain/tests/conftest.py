import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker


@pytest.fixture
def user():
    return baker.make(get_user_model())


@pytest.fixture
def data_set():
    return baker.make("catalog.DataSet")
