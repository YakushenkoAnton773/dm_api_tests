from datetime import datetime
from checkers.http_checkers import check_status_code_http
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
)



def test_get_v1_account_auth(
        auth_account_helper
):
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with("mystery"))),
                has_property('resource', has_property('registration', instance_of(datetime)))
            )
        )


def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
