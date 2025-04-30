import allure


@allure.suite("Тесты на проверку метода DELETE v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestsDeleteV1AccountLogin:
    @allure.title("Проверка разлогина пользователя")
    def test_delete_v1_account_login(
            self,
            auth_account_helper
    ):
        auth_account_helper.logout_user()
