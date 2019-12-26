import unittest
import requests
import json
from nose.tools import assert_true, assert_false

from test_services import get_response
from ..resources import models as m

header = {'Authorization': "Bearer XVRI1N9r4S4P5kTxRAAb0ntmINpTwO"}

def test_get_coach():
    param = {'id': '1'}
    response = get_response('coaches', param, header, 'get')
    assert_true(response)
    check_response(response)


def test_get_coaches():
    response = get_response('coaches', {}, header, 'get')
    assert_true(response)
    check_response(response)


def test_get_numberof_coaches():
    param = {'start_index': '1', 'number': '2'}
    response = get_response('coaches', param, header, 'get')
    assert_true(response)
    check_response(response)


def check_response(response):
    if response:
        coach_json = response.json()
        for coach_inner in coach_json:
            user = m.User(**{k: coach_inner[0][k] for k in ('date_joined', 'email', 'first_name', 'id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'last_name', 'username') if k in coach_inner[0]})
            coach = m.Coach(**{k: coach_inner[1][k] for k in ('id', 'workplace') if k in coach_inner[1]})
            assert_true(user.id >= 0)
            assert_true(coach.id >= 0)


def test_delete_coach():
    param = {'id': '1'}
    response = get_response('coaches', param, header, 'delete')
    assert_true(response)
    response = get_response('coaches', param, header, 'get')
    assert_false(response)


def test_post_coach():
    param = {'id': '1', 'workplace': 'Haarlem'}
    response = get_response('coaches', param, header, 'post')
    assert_true(response)
    if response:
        coach_json = response.json()
        coach_inner = coach_json[0]
        assert_true(coach_inner[1]['id'] == 1)
        assert_true(coach_inner[1]['workplace'] == 'Haarlem')


def test_put_coach():
    param = {'id': '1', 'workplace': 'Amsterdam'}
    response = get_response('coaches', param, header, 'put')
    assert_true(response)
    if response:
        coach_json = response.json()
        coach_inner = coach_json[0]
        assert_true(coach_inner[1]['id'] == 1)
        assert_true(coach_inner[1]['workplace'] == 'Amsterdam')