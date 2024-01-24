# Example usage
# module = PrimitiveCreationModule(
#     primitive_type=int,
# )
#
# result = module.forward("Generate an integer that represents the number of planets in our solar system.")
#
# print(f"The number of planets in the solar system is {result}")
from src.rdddy.generators.gen_python_primitive import GenPythonPrimitive

module = GenPythonPrimitive(
    primitive_type=list,
)

result = module.forward(
    "Create a list of planets in our solar system sorted by largest to smallest"
)

print(f"The number of planets in the solar system is {result}")
