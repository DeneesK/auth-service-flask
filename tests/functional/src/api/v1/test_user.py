from http import HTTPStatus

import pytest

# All test coroutines will be treated as marked with this decorator.
pytestmark = pytest.mark.asyncio


async def test_user_create(make_request):
    response = await make_request('post')(
        'users',
        json={'login': 'test_user', 'password': 'test_pass'},
    )
    assert response.status == HTTPStatus.CREATED
