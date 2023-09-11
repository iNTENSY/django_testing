from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, args',
    (
            ('news:detail', pytest.lazy_fixture('news_pk_for_args')),
            ('news:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
    )
)
@pytest.mark.django_db
def test_page_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
            (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
            (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
    ),
    ids=('AUTHOR', 'READER')
)
@pytest.mark.parametrize(
    'name, args',
    (
            ('news:edit', pytest.lazy_fixture('comment_pk_for_args')),
            ('news:delete', pytest.lazy_fixture('comment_pk_for_args')),
    ),
    ids=('EditComment', 'DeleteComment')
)
def test_pages_availability_for_author_or_anonymous_user(
        parametrized_client, expected_status, name, args
):
    url = reverse(name, args=args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
            ('news:edit', pytest.lazy_fixture('comment_pk_for_args')),
            ('news:delete', pytest.lazy_fixture('comment_pk_for_args')),
    )
)
@pytest.mark.django_db
def test_redirects(client, name, args):
    url = reverse(name, args=args)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)






