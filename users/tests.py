import json

from django.test import TestCase

USER = {'name': 'NameTest', 'age': 20, 'email': 'test@email.com'}

TRANSACTIONS = [
	{'account': 'C00099', 'date': '2020-01-03', 'amount': '-51.13', 'type': 'outflow', 'category': 'groceries'},
	{'account': 'C00099', 'date': '2020-01-10', 'amount': '2500.72', 'type': 'inflow', 'category': 'salary'},
	{'account': 'C00099', 'date': '2020-01-10', 'amount': '-150.72', 'type': 'outflow', 'category': 'transfer'},
	{'account': 'C00099', 'date': '2020-01-13', 'amount': '-560.00', 'type': 'outflow', 'category': 'rent'},
	{'account': 'C00099', 'date': '2020-01-04', 'amount': '-51.13', 'type': 'outflow', 'category': 'other'},
	{'account': 'S00012', 'date': '2020-01-10', 'amount': '150.72', 'type': 'inflow', 'category': 'savings'},
	{'account': 'S00012', 'date': '2020-01-10', 'amount': '150.72', 'type': 'inflow', 'category': 'savings'}
]

DATE_RANGE = {
	'date_start': '2020-01-01',
	'date_end': '2020-01-08'
}
ACCOUNT_SUMMARY_FILTERED_BY_DATE_EXPECTED = [
    {
        'account': 'C00099',
        'balance': -102.26,
        'total_inflow': 0,
        'total_outflow': -102.26
    }
]


ACCOUNTS_SUMMARY_EXPECTED = [
    {
        'account': 'C00099',
        'balance': 1687.74,
        'total_inflow': 2500.72,
        'total_outflow': -812.98
    },
    {
        'account': 'S00012',
        'balance': 301.44,
        'total_inflow': 301.44,
        'total_outflow': 0
    }
]

CATEGORIZED_EXPECTED = {
    'inflow': {
        'salary': 2500.72,
        'savings': 301.44
    },
    'outflow': {
        'groceries': -51.13,
        'transfer': -150.72,
        'rent': -560.0,
        'other': -51.13
    }
}
USERS_URL = '/users/'
USER_SPECIFIC_URL = USERS_URL + '%s/' 
TRANSACTIONS_URL = USER_SPECIFIC_URL + 'transactions'
ACCOUNTS_SUMMARY_URL = USER_SPECIFIC_URL + 'accounts-summary'
CATEGORIZED_URL = USER_SPECIFIC_URL + 'categorized'


class UserTestCase(TestCase):

	def test_create_user(self):
		user_creation_response = self.client.post(USERS_URL, USER)
		self.assertEquals(user_creation_response.status_code, 201)

	def test_get_users(self):
		user_list_response = self.client.get(USERS_URL)
		self.assertEquals(user_list_response.content,  b'[]')

	def test_create_and_get_user(self):
		user_creation_response = self.client.post(USERS_URL, USER)
		self.assertEquals(user_creation_response.status_code, 201)
		user_id = user_creation_response.json()['id']
		self.assertTrue(user_id > 0)

		user_response = self.client.get(USER_SPECIFIC_URL % user_id)
		self.assertTrue(user_response.status_code, 200)

		user_list_response = self.client.get(USERS_URL)
		self.assertTrue(user_response.json() in user_list_response.json())

	def test_create_user_add_transactions_get_summaries(self):
		user_creation_response = self.client.post(USERS_URL, USER)
		user_id = user_creation_response.json()['id']

		print(TRANSACTIONS_URL % user_id)
		transactions_response = self.client.post(TRANSACTIONS_URL % user_id, json.dumps(TRANSACTIONS), content_type='application/json')
		self.assertEquals(transactions_response.status_code, 200)

		user_response = self.client.get(USER_SPECIFIC_URL % user_id)
		self.assertTrue(user_response.status_code, 200)
		self.assertTrue(len(user_response.json()['transactions']) == len(TRANSACTIONS))

		accounts_summary_response = self.client.post(ACCOUNTS_SUMMARY_URL % user_id)
		self.assertEquals(accounts_summary_response.status_code, 200)
		self.assertEquals(accounts_summary_response.json(), ACCOUNTS_SUMMARY_EXPECTED)

		accounts_summary_response = self.client.post(ACCOUNTS_SUMMARY_URL % user_id, DATE_RANGE)
		self.assertEquals(accounts_summary_response.status_code, 200)
		self.assertEquals(accounts_summary_response.json(), ACCOUNT_SUMMARY_FILTERED_BY_DATE_EXPECTED)

		categorized_response = self.client.get(CATEGORIZED_URL % user_id)
		self.assertEquals(categorized_response.status_code, 200)
		self.assertEquals(categorized_response.json(), CATEGORIZED_EXPECTED)


