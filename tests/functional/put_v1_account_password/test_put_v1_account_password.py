import allure


@allure.suite("Тесты на проверку метода PUT v1/account/password")
@allure.sub_suite("Позитивные тесты")
class TestsPostV1AccountPassword:
    @allure.title("Проверка смены пароля зарегистрированного пользователя")
    def test_put_v1_account_password(self,account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        new_password = prepare_user.password + '!'
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
        account_helper.change_password(login=login, old_password=password, new_password=new_password, email=email)
        account_helper.user_login(login=login, password=new_password)
