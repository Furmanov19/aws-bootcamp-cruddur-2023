from datetime import datetime, timedelta, timezone
# from aws_xray_sdk.core import xray_recorder
from lib.db import pool, query_wrap_object, query_wrap_array

class HomeActivities:
  def run(cognito_user_id=None):
    # logger.info("HomeActivities.run()")
    # segment = xray_recorder.begin_segment('home_activities')
    # dict = {
    #   "a":"A"
    # }
    # segment.put_metadata('key', dict, 'namespace')

    # sub_segment = xray_recorder.begin_subsegment('home_activities_sub')
    # sub_segment.put_metadata('key', dict, 'namespace')

    # xray_recorder.end_subsegment();
    
    sql = query_wrap_array("""
    SELECT
      activities.uuid,
      users.display_name,
      users.handle,
      activities.message,
      activities.replies_count,
      activities.reposts_count,
      activities.likes_count,
      activities.reply_to_activity_uuid,
      activities.expires_at,
      activities.created_at
    FROM public.activities
    LEFT JOIN public.users ON users.uuid = activities.user_uuid
    ORDER BY activities.created_at DESC
    """)
    print(sql)
    with pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql)
        # this will return a tuple
        # the first field being the data
        json = cur.fetchone()
    return json[0]