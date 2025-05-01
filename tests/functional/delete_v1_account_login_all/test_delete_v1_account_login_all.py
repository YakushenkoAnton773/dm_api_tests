import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login/all")
@allure.sub_suite("Позитивные тесты")
class TestsDeleteV1AccountLoginAll:
    @allure.title("Разлогин всех пользователей")
    def test_delete_v1_account_login_all(
            self,
            auth_account_helper
    ):
        auth_account_helper.logout_all_users()
