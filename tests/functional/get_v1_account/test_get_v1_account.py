def test_get_v1_account_auth(auth_account_helper):
    auth_account_helper.dm_account_api.account_api.get_v1_account()


def test_get_v1_account_no_auth(account_helper):
    resp = account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
    assert resp.status_code == 401, f"Ожидали 401 Unauthorized, получили {resp.status_code}"
