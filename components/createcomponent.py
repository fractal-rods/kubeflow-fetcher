import kfp.components as comp


def add(a: float, b: float) -> float:
    """Calculates sum of two arguments"""
    return a + b


if __name__ == "__main__":
    comp.create_component_from_func(
        func=add, output_component_file="add_component.yaml"
    )
