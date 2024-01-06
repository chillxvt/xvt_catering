from django.test import TestCase

# Create your tests here.
JSON = {

    "meals": [
        {
            "id": 24,
            "date": "2024-01-02",
            "meal": "lu",
            "dishes": [
                {
                    "id": 19,
                    "recipe": {
                        "id": 40,
                        "name": "Grilled Chicken",
                        "instructions": "Marinate chicken, grill until fully cooked.",
                        "ingredients": [
                            {
                                "ingredient": {
                                    "id": 32,
                                    "name": "Chicken Breast"
                                },
                                "unit": "g",
                                "amount": 200.0
                            },
                            {
                                "ingredient": {
                                    "id": 33,
                                    "name": "Olive Oil"
                                },
                                "unit": "ml",
                                "amount": 30.0
                            },
                            {
                                "ingredient": {
                                    "id": 34,
                                    "name": "Rosemary"
                                },
                                "unit": "g",
                                "amount": 10.0
                            }
                        ]
                    },
                    "portions": 3
                },
                {
                    "id": 20,
                    "recipe": {
                        "id": 41,
                        "name": "Quinoa Salad",
                        "instructions": "Mix cooked quinoa with vegetables and dressing.",
                        "ingredients": [
                            {
                                "ingredient": {
                                    "id": 35,
                                    "name": "Quinoa"
                                },
                                "unit": "g",
                                "amount": 150.0
                            },
                            {
                                "ingredient": {
                                    "id": 36,
                                    "name": "Cherry Tomatoes"
                                },
                                "unit": "g",
                                "amount": 50.0
                            },
                            {
                                "ingredient": {
                                    "id": 37,
                                    "name": "Cucumber"
                                },
                                "unit": "g",
                                "amount": 30.0
                            },
                            {
                                "ingredient": {
                                    "id": 38,
                                    "name": "Balsamic Vinaigrette"
                                },
                                "unit": "ml",
                                "amount": 45.0
                            }
                        ]
                    },
                    "portions": 2
                }
            ],
            "extras": [
                {
                    "id": 35,
                    "item": {
                        "id": 39,
                        "name": "Green Tea"
                    },
                    "unit": "ml",
                    "amount": 300.0
                },
                {
                    "id": 36,
                    "item": {
                        "id": 40,
                        "name": "Avocado"
                    },
                    "unit": "unt",
                    "amount": 1.0
                }
            ]
        },
        {
            "id": 25,
            "date": "2024-01-02",
            "meal": "lu",
            "dishes": [],
            "extras": [
                {
                    "id": 37,
                    "item": {
                        "id": 39,
                        "name": "Green Tea"
                    },
                    "unit": "ml",
                    "amount": 300.0
                },
                {
                    "id": 38,
                    "item": {
                        "id": 40,
                        "name": "Avocado"
                    },
                    "unit": "unt",
                    "amount": 1.0
                }
            ]
        },
        {
            "id": 26,
            "date": "2024-01-02",
            "meal": "lu",
            "dishes": [],
            "extras": [
                {
                    "id": 39,
                    "item": {
                        "id": 39,
                        "name": "Green Tea"
                    },
                    "unit": "ml",
                    "amount": 300.0
                },
                {
                    "id": 40,
                    "item": {
                        "id": 40,
                        "name": "Avocado"
                    },
                    "unit": "unt",
                    "amount": 1.0
                }
            ]
        },
        {
            "id": 27,
            "date": "2024-01-02",
            "meal": "lu",
            "dishes": [],
            "extras": [
                {
                    "id": 41,
                    "item": {
                        "id": 39,
                        "name": "Green Tea"
                    },
                    "unit": "ml",
                    "amount": 300.0
                },
                {
                    "id": 42,
                    "item": {
                        "id": 40,
                        "name": "Avocado"
                    },
                    "unit": "unt",
                    "amount": 1.0
                }
            ]
        },
        {
            "id": 28,
            "date": "2024-01-02",
            "meal": "lu",
            "dishes": [],
            "extras": [
                {
                    "id": 43,
                    "item": {
                        "id": 39,
                        "name": "Green Tea"
                    },
                    "unit": "ml",
                    "amount": 300.0
                },
                {
                    "id": 44,
                    "item": {
                        "id": 40,
                        "name": "Avocado"
                    },
                    "unit": "unt",
                    "amount": 1.0
                }
            ]
        },
        {
            "id": 29,
            "date": "2024-01-02",
            "meal": "lu",
            "dishes": [],
            "extras": [
                {
                    "id": 45,
                    "item": {
                        "id": 39,
                        "name": "Green Tea"
                    },
                    "unit": "ml",
                    "amount": 300.0
                },
                {
                    "id": 46,
                    "item": {
                        "id": 40,
                        "name": "Avocado"
                    },
                    "unit": "unt",
                    "amount": 1.0
                }
            ]
        }
    ]
}