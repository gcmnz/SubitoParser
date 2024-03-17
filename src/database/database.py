import sqlite3
from datetime import datetime, timedelta


class AccountDatabase:
    def __init__(self):
        if __name__ == '__main__':
            db_path = 'accounts.db'
        else:
            db_path = 'src/database/accounts.db'
        print(db_path)
        self.__connection = sqlite3.connect(db_path, check_same_thread=False)
        self.__cursor = self.__connection.cursor()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()

    def create_table(self, *args):
        """
        usage: create_table(table_name, column_names ...)
        example: create_table('Accounts', 'login', 'password', 'online_status')
        """

        # открываем базу
        with self.__connection:
            # получаем количество таблиц с нужным нам именем
            data = self.__connection.execute(
                f"select count(*) from sqlite_master where type='table' and name='{args[0]}'")
            for row in data:
                # если таких таблиц нет
                if row[0] == 0:
                    # создаём таблицу
                    with self.__connection:
                        names = ''
                        for name in args[1:]:
                            if name == args[-1]:
                                names += f'{name} VARCHAR'
                            else:
                                names += f'{name} VARCHAR,\n'

                        self.__connection.execute(f"""
                            CREATE TABLE {args[0]} (
                                {names}
                            );
                        """)

    def _clear_table(self):
        with self.__connection:
            self.__cursor.execute("DELETE FROM Accounts")

    def add_user(self, user_id: int):
        with self.__connection:
            self.__cursor.execute("INSERT INTO Accounts (user_id, state, subscribe, balance) VALUES (?, ?, ?, ?)", (user_id, 'main', datetime.now(), 0))

    def user_exists(self, user_id: int):
        with self.__connection:
            result = self.__cursor.execute('SELECT * FROM Accounts WHERE user_id = ?', (user_id,)).fetchall()
            return bool(result)

    def get_state(self, user_id: int) -> str:
        with self.__connection:
            result = self.__cursor.execute('SELECT state FROM Accounts WHERE user_id = ?', (user_id,)).fetchone()
            if result is None:
                return 'None'
            return result[0]

    def set_state(self, user_id: int, state: str):
        with self.__connection:
            return self.__cursor.execute('UPDATE Accounts SET state = ? WHERE user_id = ?', (state, user_id,))

    def get_subscribe(self, user_id: int):
        with self.__connection:
            current_subscribe_time = self.__cursor.execute('SELECT subscribe FROM Accounts WHERE user_id = ?', (user_id,)).fetchone()[0]
            return datetime.fromisoformat(current_subscribe_time)

    def set_subscribe(self, user_id: int, time_):
        with self.__connection:
            return self.__cursor.execute('UPDATE Accounts SET subscribe = ? WHERE user_id = ?', (time_, user_id,))

    def add_subscribe(self, user_id: int, days: int):
        now_time = datetime.now()
        subscribe_time = now_time + timedelta(days=days)

        with self.__connection:
            self.__cursor.execute('UPDATE Accounts SET subscribe = ? WHERE user_id = ?', (subscribe_time, user_id,))
            return subscribe_time.strftime('%d.%m.%Y %H:%M:%S')

    def is_subscribe_valid(self, user_id: int) -> bool:
        with self.__connection:
            subscribe_time_str = self.__cursor.execute('SELECT subscribe FROM Accounts WHERE user_id = ?', (user_id,)).fetchone()[0]
            subscribe_time = datetime.fromisoformat(subscribe_time_str)
            return subscribe_time >= datetime.now()

    def get_balance(self, user_id: int) -> int:
        with self.__connection:
            result = self.__cursor.execute('SELECT balance FROM Accounts WHERE user_id = ?', (user_id,)).fetchone()[0]
            return int(result)

    def set_balance(self, user_id: int, balance):
        with self.__connection:
            return self.__cursor.execute('UPDATE Accounts SET balance = ? WHERE user_id = ?', (balance, user_id,))


if __name__ == '__main__':
    database = AccountDatabase()
    # database.create_table('Accounts', 'user_id', 'state', 'subscribe', 'balance')
    # database._clear_table()
    database.set_balance(1580689542, 100)
