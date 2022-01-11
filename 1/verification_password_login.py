from database import DataBase


class VerificationPasswordLogin(object):
    class __LoginException(Exception):
        pass

    class __PasswordException(Exception):
        pass

    @classmethod
    def set_verification_password_login(cls, username: str = "", password: str = "", special_key: str = ""):
        try:
            login_db, password_db = DataBase.get_verification_password_login_db(username)

            if username == login_db:
                if (password, None) == password_db:
                    return True
                elif (password, special_key) == password_db:
                    return "incasation"
                else:
                    raise cls.__PasswordException(f"<incorrect password -> {password}>")
            else:
                raise cls.__LoginException(f"<incorrect login -> {username}>")

        except IndexError:
            print(f"<status incorrect login -> {username}>")
        except cls.__LoginException as err:
            print(f"<status incorrect login -> {err}>")
        except cls.__PasswordException as err:
            print(f"<status incorrect password -> {err}>")


