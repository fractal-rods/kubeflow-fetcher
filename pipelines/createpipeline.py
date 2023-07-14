import kfp.dsl as dsl
import kfp.components 
import kfp.compiler 

add_op = kfp.components.load_component("components/add_component.yaml")

@dsl.pipeline(
  name='Addition pipeline',
  description='An example pipeline that performs addition calculations.'
)
def add_pipeline(
  a='5',
  b='7',
):
  # Passes a pipeline parameter and a constant value to the `add_op` factory
  # function.
  add_task = add_op(a, b)

kfp.compiler.Compiler().compile(
    pipeline_func=add_pipeline,
    package_path='add_pipeline.yaml'
    )