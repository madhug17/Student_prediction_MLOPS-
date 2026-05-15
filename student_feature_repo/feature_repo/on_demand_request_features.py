import pandas as pd

from feast import Field, RequestSource
from feast.types import Float32, Int64
from feast.on_demand_feature_view import on_demand_feature_view

from feature_definition import student_features


# LIVE REQUEST DATA
live_input = RequestSource(
    name="live_input",
    schema=[
        Field(name="hours_slept", dtype=Int64),
        Field(name="extra_study_hours", dtype=Int64),
    ],
)


# ON-DEMAND REQUEST FEATURE VIEW
@on_demand_feature_view(
    sources=[student_features, live_input],
    schema=[
        Field(name="live_performance_score", dtype=Float32),
    ],
)
def student_request_metrics(inputs: pd.DataFrame) -> pd.DataFrame:

    inputs["live_performance_score"] = (
        inputs["G2"]
        + inputs["studytime"]
        + inputs["extra_study_hours"]
        + inputs["hours_slept"]
    ) / 4

    return pd.DataFrame.from_dict({
        "live_performance_score": inputs["live_performance_score"].astype("float32"),
    })