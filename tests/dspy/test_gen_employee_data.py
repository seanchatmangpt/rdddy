import os

import inspect


from typing import List, Optional
from pydantic import BaseModel

from rdddy.generators.gen_python_primitive import GenPythonPrimitive


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str


class Employee(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: str
    skills: List[str]
    address: Address
    is_manager: Optional[bool] = False


# Complex string describing an Employee instance
employee_description = f"""
Alex Johnson is 35 years old. His email is alex.johnson@example.com. 
He has skills in Python, JavaScript, and SQL. His address is 123 Main St, Springfield, IL, 62704, USA. 
Alex is not a manager. 
{inspect.getsource(Address)}
{inspect.getsource(Employee)}
"""


module = GenPythonPrimitive(primitive_type=dict)

result = module.forward(employee_description)

print(f"{employee_description}: {Employee(**result)}")
