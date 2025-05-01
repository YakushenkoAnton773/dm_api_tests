import allure


@allure.suite("Тесты на проверку метода POST v1/account/login")
@allure.sub_suite("Позитивные тесты")
class TestsPostV1AccountLogin:
    @allure.title("Авторизация пользователя")
    def test_post_v1_account_login(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, email=email, password=password)
        account_helper.user_login(login=login, password=password)
