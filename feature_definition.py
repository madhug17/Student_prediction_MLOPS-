from datetime import timedelta
from feast import (
    Entity,
    FeatureView,
    Field,
    ValueType,
    FeatureService,
)
from feast.types import Int64
from feast.infra.offline_stores.file_source import FileSource

student = Entity(
    name="student_id",
    join_keys=["student_id"],
    value_type=ValueType.INT64
)

student_source = FileSource(
    path="data/student_data.parquet",
    timestamp_field="event_timestamp"
)

student_features = FeatureView(
    name="student_features",
    entities=[student],
    ttl=timedelta(days=1),
    schema=[
        Field(name="absences", dtype=Int64),
        Field(name="studytime", dtype=Int64),
        Field(name="G2", dtype=Int64),
    ],
    online=True,
    source=student_source,
)

student_prediction_service = FeatureService(
    name="student_prediction_service",
    features=[student_features]
)