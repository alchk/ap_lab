import unittest

import sqlalchemy

from app import app
from base64 import b64encode
import json
from models import engine


class TestBase(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    tester = app.test_client()
    creds = b64encode(b"nulltwo:password").decode('utf-8')

class UserApiTest(TestBase):

    data = {
        "first_name": "Lol",
        "last_name": "Kek",
        "password": "password",
        "user_name": "nulltwo"
    }

    def test_user_create(self):
        clean_db()
        response = self.tester.post('/api/v1/users', data=json.dumps(self.data), content_type='application/json')
        code = response.status_code
        self.assertEqual(201, code)

    def test_create_user_with_invalid_data(self):
        clean_db()
        response = self.tester.post('/api/v1/users', data=json.dumps({"user_name":23423432042343243242423}), content_type ='application/json')
        code = response.status_code
        self.assertEqual(405, code)

    def test_get_user_by_id(self):
        clean_db()
        insert_user()
        response = self.tester.get('/api/v1/users', headers={"Authorization":f"Basic {self.creds}"})

        code = response.status_code
        self.assertEqual(200, code)

    def test_unauthorized(self):
        clean_db()
        insert_user()
        response = self.tester.get('/api/v1/users', headers={"Authorization": "Basic lol:keke"})

        code = response.status_code
        self.assertEqual(401, code)

    def test_update(self):
        clean_db()
        insert_user()
        response = self.tester.put('/api/v1/users/1',
                                   data = json.dumps({"user_name": "lol"}),
                                   content_type ='application/json',
                                   headers={"Authorization": f"Basic {self.creds}"})

        code = response.status_code
        self.assertEqual(200, code)
class WalletApiTest(TestBase):

    wallet_data = {
        "user_id": 1
    }

    def test_wallet_creation(self):
        clean_db()
        insert_user()
        response = self.tester.post('/api/v1/wallets',
                                    data = json.dumps(self.wallet_data),
                                    content_type = 'application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(201, code)

    def test_unauthorized_wallet_creation(self):
        clean_db()
        insert_user()
        response = self.tester.post('/api/v1/wallets',
                                    data = json.dumps({"user_id":232}),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"})
        code = response.status_code
        self.assertEqual(401, code)

    def test_wallet_top_up(self):
        clean_db()
        insert_user()
        insert_wallet()
        response = self.tester.put('/api/v1/wallets/1',
                                    data = json.dumps({"balance":50}),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"}
                                    )
        code = response.status_code
        self.assertEqual(200, code)

    def test_get_user_wallets(self):
        clean_db()
        insert_user()
        insert_wallet()
        response = self.tester.get('/api/v1/wallets',
                                   headers={"Authorization": f"Basic {self.creds}"}
                                   )
        code = response.status_code
        self.assertEqual(200, code)

class TransactionApiTest(TestBase):

    transaction_data = {
            "sender_id": 1,
            "receiver_id": 2,
            "amount": 50
    }

    bad_transaction_data = {
        "sender_id": 1,
        "receiver_id": 2,
        "amount": 1000000
    }

    def test_transaction(self):
        clean_db()
        insert_user()
        insert_wallet()

        response = self.tester.post('/api/v1/transactions',
                                    data = json.dumps(self.transaction_data),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"}
                                    )

        code = response.status_code
        self.assertEqual(code, 201)

    def test_unauthorized_amount(self):
        clean_db()
        insert_user()
        insert_wallet()
        response = self.tester.post('/api/v1/transactions',
                                    data=json.dumps(self.transaction_data),
                                    content_type='application/json',
                                    headers={"Authorization": "Basic lol:keke"}
                                    )

        code = response.status_code
        self.assertEqual(401, code)


    def test_invalid_transaction(self):
        clean_db()
        insert_user()
        insert_wallet()
        response = self.tester.post('/api/v1/transactions',
                                    data=json.dumps(self.bad_transaction_data),
                                    content_type='application/json',
                                    headers={"Authorization": f"Basic {self.creds}"}
                                    )

        code = response.status_code
        self.assertEqual(405, code)

def clean_db():
    clean_file = open('/Users/ivanalchuk/Desktop/ap_lab/sql/clean_db.sql')
    clean_sql = sqlalchemy.text(clean_file.read())
    engine.execute(clean_sql)
    clean_file.close()

def insert_user():
    insert_file = open('/Users/ivanalchuk/Desktop/ap_lab/sql/insert_user.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()

def insert_wallet():
    insert_file = open('/Users/ivanalchuk/Desktop/ap_lab/sql/insert_wallet.sql')
    insert = sqlalchemy.text(insert_file.read())
    engine.execute(insert)
    insert_file.close()



if __name__ == '__main__':
    unittest.main()


#run with coverage coverage run --omit '/Users/ivanalchuk/Desktop/ap_lab/ap_env/*' -m unittest api_test.py && coverage report -m