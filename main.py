from fastapi import FastAPI, Request, Response
from urllib import parse

app = FastAPI()


# 104974212406042

PAGE_ACCESS_TOKEN = "EAAaa0R8dEFABAAEZBhhZBfrjNcUr5huRa88Hx9TZCw5YLP17GExvWuh5z7ftN1x0TRloFt2GfFEc2cwZAj3C1K0wqxRDSJgRYrZALNd2MQe5gu19d08jCwaBZAstmbVuUmZBt26PMATX7WwqL6rit3ZAqZBLDWDGY3htnA7ynPW53HWuvoApEeZAYq0olJO8cDZCrEKuMZCYRuGPYwZDZD"


# curl -X GET "localhost:1337/webhook?hub.verify_token=YOUR-VERIFY-TOKEN&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe"

@app.get("/")
async def index(request: Request):
    params = request.query_params
    if params.get("hub.mod") == 'subscribe'  and params.get('hub.challenge'):
        if not params.get("hub.verify_token") == "btsl":
            return Response('invalid token', status_code=403)
    return Response(params['hub.challenge'], status_code=200)

@app.post("/")
async def fbwebhook(request: Request):
    await request.json()
    return True


# ==== Query
#   curl -i -X GET \
#    "https://graph.facebook.com/v15.0/me?fields=category%2Capp_id%2Cname%2Cphotos%7Blink%2Cheight%2Cwidth%7D%2Cemails%2Clink%2Cabout&access_token=<access token sanitized>"
# ==== Access Token Info
#   {
#     "perms": [
#       "pages_manage_cta",
#       "pages_manage_instant_articles",
#       "pages_show_list",
#       "read_page_mailboxes",
#       "ads_management",
#       "ads_read",
#       "business_management",
#       "pages_messaging",
#       "pages_messaging_phone_number",
#       "pages_messaging_subscriptions",
#       "publish_to_groups",
#       "groups_access_member_info",
#       "attribution_read",
#       "page_events",
#       "pages_read_engagement",
#       "pages_manage_metadata",
#       "pages_read_user_content",
#       "pages_manage_ads",
#       "pages_manage_posts",
#       "pages_manage_engagement",
#       "public_profile"
#     ],
#     "page_id": 104974212406042,
#     "user_id": 5814100952015822,
#     "app_id": 605272124535396
#   }
# ==== Parameters
# - Query Parameters


#   {
#     "fields": "category,app_id,name,photos{link,height,width},emails,link,about"
#   }
# - POST Parameters


#   {}
# ==== Response
#   {
#     "category": "Software company",
#     "name": "Bright Tech Solutions Ltd.",
#     "photos": {
#       "data": [
#         {
#           "link": "https://www.facebook.com/photo.php?fbid=101099809469551&set=a.101091902803675&type=3",
#           "height": 640,
#           "width": 724,
#           "id": "101099809469551"
#         },
#         {
#           "link": "https://www.facebook.com/photo.php?fbid=101091889470343&set=a.101091902803675&type=3",
#           "height": 1290,
#           "width": 1290,
#           "id": "101091889470343"
#         }
#       ],
#       "paging": {
#         "cursors": {
#           "before": "QVFIUi01ZATQtcDJlRzhFYi15RF9BdTNNeE1DUnlEYjlidnNNMlhydzNuWnpDY2Q2emRwa21xY2tYZAnFpY3FkRzNlaUVsUmZAGM2NGblYzU0RTUzQ4Q0xPNU5R",
#           "after": "QVFIUi0weTEwYWQwcWlRUUJhRm5Wal9MZA0ZAVcjMzREZAaZAEMxMTg2SFU5X1MwYnBaUmFYUmU4MnZADNlQ5WjBHM3V0RVMwYXhsa21yT1p2blFpQnZAFdFh6cWdn"
#         }
#       }
#     },
#     "emails": [
#       "faahad.hossain@gmail.com"
#     ],
#     "link": "https://www.facebook.com/104974212406042",
#     "about": "An unimaginary Tech footstep at your neighbourhood",
#     "id": "104974212406042"
#   }