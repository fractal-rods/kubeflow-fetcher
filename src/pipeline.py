import kfp
from kfp import dsl
import kfp.components as comp

# components need to be loaded before pipeline definition not inside the pipeline!
lake_op = comp.load_component_from_file("lakefs/component.yaml")


@dsl.pipeline(
    name="lakefs demo pipeline", description="demo pipeline for modifying lakefs data"
)
def lakefs_modify_pipeline(
    lake_host: str = "",
    lake_id: str = "",
    lake_token: str = "",
):
    modify_data_step = lake_op(host=lake_host, id=lake_id, token=lake_token)

    return modify_data_step


if __name__ == "__main__":
    kfp.compiler.Compiler().compile(lakefs_modify_pipeline, "pipeline.yaml")
