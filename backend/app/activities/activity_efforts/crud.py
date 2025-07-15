from activities.activity.crud import get_activities_by_interval
from backend.app.activities.activity_streams.crud import transform_activity_streams_hr
from sqlalchemy.orm import Session
from typing import Annotated, Callable, Optional
import activities.activity_efforts.schema as activity_efforts_schema
import activities.activity_streams.models as activity_streams_models
import activities.activity_streams.constants as activity_streams_constants
import session.security as session_security
import core.database as core_database


def get_efforts(
    db: Session, 
    user_id: int, 
    activity_type: int,
    date: str,
    interval: str
) -> list[activity_efforts_schema.RelativeEffort]:
    """
    Fetches relative efforts for a user on a specific date.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user.
        date (str): Date in 'YYYY-MM-DD' format.

    Returns:
        list[activity_efforts_schema.RelativeEffort]: List of relative efforts.
    """
    # Placeholder for actual implementation

    activities = get_activities_by_interval(
        db=db,
        user_id=user_id,
        activity_type=activity_type,  # Assuming 1 is the activity type for relative efforts
        interval=interval,
        date=date
    )

    print(f"Activities: {activities}")

    relative_efforts = []
    for activity in activities:

        activity_stream_hr = db.query(activity_streams_models.ActivityStreams).filter(
            activity_streams_models.ActivityStreams.activity_id == activity.id,
            activity_streams_models.ActivityStreams.stream_type == activity_streams_constants.STREAM_TYPE_HR,
        ).all()

        translated = transform_activity_streams_hr(activity_stream_hr, activity, db)

        print(activity)

        relative_efforts.append(
            activity_efforts_schema.RelativeEffort(
                relative_effort=translated.relative_effort,  # Assuming this field exists
                activity_id=activity.id,
                date=date
            )
        )

    return relative_efforts