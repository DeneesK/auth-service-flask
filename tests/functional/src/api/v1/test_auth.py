from http import HTTPStatus

import pytest

# All test coroutines will be treated as marked with this decorator.
pytestmark = pytest.mark.asyncio


async def test_login_wrong_data(make_request):
    response = await make_request('post')('auth/login', json={'login': 'test_user'})

    assert response.status == HTTPStatus.BAD_REQUEST
    assert 'password' in response.body


async def test_login_not_exists(make_request):
    response = await make_request('post')(
        'auth/login', json={'login': 'test_user', 'password': 'test_pass'}
    )

    assert response.status == HTTPStatus.FORBIDDEN
    assert response.body == ''


async def test_login(make_request, user):
    response = await make_request('post')(
        'auth/login', json={'login': 'test_user', 'password': 'test_pass'}
    )

    assert response.status == HTTPStatus.OK
    assert set(response.body.keys()) == set(['access', 'refresh'])
