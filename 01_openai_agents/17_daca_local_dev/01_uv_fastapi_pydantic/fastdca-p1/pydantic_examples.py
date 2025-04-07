
# ------------------------------------------------------------------------------------------------
# STEP 1: TRY THE FOLLOWING ERROR CODE
# ------------------------------------------------------------------------------------------------
# from pydantic import BaseModel, ValidationError

# # Define a simple model
# class User(BaseModel):
#     id: int
#     name: str
#     email: str
#     age: int | None = None  # Optional field with default None

# # Valid data
# user_data = {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25}
# user = User(**user_data)
# print(user)  # id=1 name='Alice' email='alice@example.com' age=25
# print(user.model_dump())  # {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'age': 25}

# # Invalid data (will raise an error)
# try:
#     invalid_user = User(id="not_an_int", name="Bob", email="bob@example.com")
# except ValidationError as e:
#     print(e)


# ------------------------------------------------------------------------------------------------
# # STEP 2: TRY THE FOLLOWING CODE
# ------------------------------------------------------------------------------------------------
# from pydantic import BaseModel, EmailStr

# # Define a nested model


# class Address(BaseModel):
#     street: str
#     city: str
#     zip_code: str


# class UserWithAddress(BaseModel):
#     id: int
#     name: str
#     email: EmailStr  # Built-in validator for email format
#     addresses: list[Address]  # List of nested Address models


# # Valid data with nested structure
# user_data = {
#     "id": 2,
#     "name": "Bob",
#     "email": "bob@example.com",
#     "addresses": [
#         {"street": "123 Main St", "city": "New York", "zip_code": "10001"},
#         {"street": "456 Oak Ave", "city": "Los Angeles", "zip_code": "90001"},
#     ],
# }
# user = UserWithAddress.model_validate(user_data)
# print(user.model_dump())


# ------------------------------------------------------------------------------------------------
# # STEP 3: TRY THE FOLLOWING CODE
# ------------------------------------------------------------------------------------------------


from pydantic import BaseModel, EmailStr, field_validator, ValidationError


class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    addresses: list[Address]

    @field_validator("name")
    def name_must_be_at_least_two_chars(cls, v):
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters long")
        return v


# Test with invalid data
try:
    invalid_user = UserWithAddress(
        id=3,
        name="A",  # Too short
        email="charlie@example.com",
        addresses=[Address(street="789 Pine Rd", city="Chicago", zip_code="60601")],
    )
except ValidationError as e:
    print(e)
