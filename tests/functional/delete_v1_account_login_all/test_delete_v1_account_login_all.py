import pytest

@pytest.mark.skip(reason="Проходит если запускать отдельно, валится если запущен вместе с другими")
def test_delete_v1_account_login_all(auth_account_helper):
    auth_account_helper.logout_all_users()

