from datetime import timedelta
from feast import (
    Entity,
    FeatureView,
    Field,
    ValueType,
    FeatureService,
    PushSource,
)
from feast.types import Int64
from feast.infra.offline_stores.file_source import FileSource


# ENTITY
student = Entity(
    name="student_id",
    join_keys=["student_id"],
    value_type=ValueType.INT64
)


# BATCH SOURCE
student_source = FileSource(
    path="data/student_data.parquet",
    timestamp_field="event_timestamp"
)


# PUSH SOURCE
student_push_source = PushSource(
    name="student_push_source",
    batch_source=student_source,
)


# FEATURE VIEW
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
    source=student_push_source,
)


# FEATURE SERVICE
student_prediction_service = FeatureService(
    name="student_prediction_service",
    features=[student_features],
)