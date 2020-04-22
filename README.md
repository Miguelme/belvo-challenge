# Belvo Challenge - Users and Transactions

Author : Miguel Fagundez / Software Engineer

## Requirements

- Docker

## Build Steps

1. First we need to build the docker image for running the application

```$ docker build . -t belvo-challenge```

2. After the image has been built correctly we can proceed to run it as follows 

```$ docker run -p 8000:8000 belvo-challenge```

When the docker container is deployed we will have available several endpoints that match the challenge requirements, 
and they will be exposed in the port 8000 as specified in the command above.

## Executing Tests 

A test suite of 4 tests was created that can be executed with the following command:
```
$ python manage.py test
```

## Exercises
1. Can create users by receiving: name, email and age

- A user can be created in the following endpoint: `/users` using a `POST` request with a payload similar to below (where we could ignore the transactions field as an empty array):

```
{
        "name": "Miguel",
        "email": "miguel@email.com",
        "age": 28,
        "transactions": [
            {
                "account": "A-1",
                "date": "2020-04-21",
                "amount": "1312312.00",
                "type": "inflow",
                "category": "A"
            },
            {
                "account": "A-1",
                "date": "2010-04-21",
                "amount": "-312312.00",
                "type": "outflow",
                "category": "B"
            },
            {
                "account": "B-1",
                "date": "2010-04-21",
                "amount": "-312312.00",
                "type": "outflow",
                "category": "B"
            }
        ]
    }
``` 
2. List all users and also and see the details of a specific user

- Users can be listed in the following endpoint: `/users` using a `GET` request.
- The details of a user can be obtained by using the following endpoint: `/users/<id>` where `<id>` is equals to the user id using a `GET` request.

3. Can save users' transactions. Each transaction has: reference (unique), account, date, amount, type and category

- Transactions for a given user can be saved in the following endpoint: `/users/<id>/transactions` where `<id>` is the user id,
 using a `POST` request with a payload similar to the one below:

```
[
  {
    "reference": "000051",
    "account": "C00099",
    "date": "2020-01-03",
    "amount": "-51.13",
    "type": "outflow",
    "category": "groceries"
  },
  {
    "reference": "000052",
    "account": "C00099",
    "date": "2020-01-10",
    "amount": "2500.72",
    "type": "inflow",
    "category": "salary"
  },
  {
    "reference": "000053",
    "account": "C00099",
    "date": "2020-01-10",
    "amount": "-150.72",
    "type": "outflow",
    "category": "transfer"
  },
  {
    "reference": "000054",
    "account": "C00099",
    "date": "2020-01-13",
    "amount": "-560.00",
    "type": "outflow",
    "category": "rent"
  },
  {
    "reference": "000055",
    "account": "C00099",
    "date": "2020-01-04",
    "amount": "-51.13",
    "type": "outflow",
    "category": "other"
  },
  {
    "reference": "000689",
    "account": "S00012",
    "date": "2020-01-10",
    "amount": "150.72",
    "type": "inflow",
    "category": "savings"
  }
]
```

## Goals
 1. Given an user id, we want to be able to see a summary by account that shows the balance of the account, 
total inflow and total outflows. It should be possible to specify a date range, 
if no date range is given all transactions should be considered

- In order to achieve this we created an endpoint `/users/<id>/accounts-summary` to be used with a `POST` requess where 
the date range can be given or no (empty `POST` request). An example of the payload is below: 
```
{
  "date_start": "2000-01-01",
  "date_end": "2019-01-01"
}
```
2. We want to be able to see a user's summary by category that shows the sum of amounts per transaction category

- In order to achieve this we created an endpoint `/users/<id>/categorized` to be used with a `GET` request 