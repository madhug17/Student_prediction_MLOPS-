from feast import Field
from feast.on_demand_feature_view import on_demand_feature_view
from feast.types import Float32
import pandas as pd
from feature_definition import student_features

@on_demand_feature_view(
    sources=[student_features],
    schema=[
        Field(name="performance_ratio", dtype=Float32),
        Field(name="attendance_score", dtype=Float32),
        Field(name="final_risk_score", dtype=Float32),
    ],
)
def student_live_metrics(inputs: pd.DataFrame) -> pd.DataFrame:

    df = pd.DataFrame()

    df["performance_ratio"] = (
        inputs["G2"] / inputs["studytime"]
    ).astype("float32")

    df["attendance_score"] = (
        100 - inputs["absences"]
    ).astype("float32")

    df["final_risk_score"] = (
        df["performance_ratio"] * 0.7 +
        df["attendance_score"] * 0.3
    ).astype("float32")

    return df