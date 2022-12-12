from http import HTTPStatus

import pytest

# All test coroutines will be treated as marked with this decorator.
pytestmark = pytest.mark.asyncio


async def test_roles_read(make_request, role_fixture):
    response = await make_request('get')('roles')
    assert response.status == HTTPStatus.OK
    assert isinstance(response.body, list)
    assert response.body[0]['id'] == role_fixture['id']
