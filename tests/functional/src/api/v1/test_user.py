import re
from http import HTTPStatus
from uuid import uuid4

import pytest

# All test coroutines will be treated as marked with this decorator.
pytestmark = pytest.mark.asyncio

USER_ID = None


async def test_user_create(make_request):
    response = await make_request('post')(
        'users',
        json={'login': 'test_user', 'password': 'test_pass'},
    )
    location_regex = (
        '.*/v1/users/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$'
    )
    location = re.match(location_regex, response.headers['location'])

    assert response.status == HTTPStatus.CREATED

    # The URI of the new resource is included in the Location header of the response.
    assert location is not None, '"{0}" doesn\'t match location regex "{1}"'.format(
        response.headers['location'],
        location_regex,
    )

    # The response body contains a representation of the resource.
    assert response.body['login'] == 'test_user'

    # Ensure we don't expose password
    assert set(response.body.keys()) == set(['id', 'login'])

    # assign user's id to global variable to use in another tests
    # this is intentionally below assertions
    global USER_ID
    USER_ID = location.group(1)


async def test_user_read_notexists(make_request):
    response = await make_request('get')('users/{0}'.format(str(uuid4())))
    assert response.status == HTTPStatus.NOT_FOUND
    assert response.body == ''


async def test_user_read(make_request):
    global USER_ID
    response = await make_request('get')('users/{0}'.format(USER_ID))
    assert response.status == HTTPStatus.OK
    assert response.body['id'] == USER_ID



async def test_user_remove(make_request):
    response = await make_request('post')(
        'users',
        json={'login': 'test_remove', 'password': 'test_pass'},
    )
    user_id = response.get_json()['id']
    
    r = await make_request('post')('users/remove',
                                   json={'id': user_id}
    )
    r2 = await make_request('post')('users/remove',
                                    json={'id': user_id}
    )
    assert r.status == HTTPStatus.OK
    assert r2.status == HTTPStatus.NOT_FOUND
    