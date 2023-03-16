from app.config.mysqlconnection import connectToMySQL


class Poke:
    db_name = 'user_db'

    def __init__(self, db_name):
        self.id = db_name['id']
        self.sender_id = db_name['sender_id']
        self.receiver_id = db_name['receiver_id']
        self.created_at = db_name['created_at']
        self.updated_at = db_name['updated_at']
        self.sender = db_name['sender']
        self.receiver = db_name['receiver']

    @classmethod
    def add_poke(cls, data):
        query = "INSERT INTO pokes (sender_id, receiver_id) VALUES (%(sender_id)s, %(receiver_id)s);"
        return connectToMySQL('db_name').query_db(query, data)

    @classmethod
    def get_pokes_of_user(cls, data):
        query = "SELECT users.name as sender, users2.name as receiver, pokes.* FROM users LEFT JOIN pokes ON users.id = pokes.sender_id LEFT JOIN users as users2 ON users2.id = pokes.receiver_id WHERE users2.id =  %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        pokes = []
        for poke in results:
            pokes.append(cls(poke))
        print(pokes)
        return pokes

    @classmethod
    def save(cls, data):
        query = "INSERT INTO pokes (sender_id,receiver_id) VALUES (%(sender_id)s,%(receiver_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def count_pokes(cls, data):
        query = "SELECT users.id, users.name, count(users.id) as 'receiver' from pokes JOIN users ON users.id = pokes.receiver_id GROUP BY users.id ORDER BY receiver DESC LIMIT 14;"
        count = connectToMySQL(cls.db_name).query_db(query, data)
        return count
