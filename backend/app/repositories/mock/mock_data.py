from copy import deepcopy
from datetime import datetime, timedelta

COMMON = {
    "created_by": 0,
    "updated_by": 0,
    "is_deleted": 0,
}

_now = datetime.now()

USERS = [
    {
        "id": 1,
        "username": "petlover01",
        "nickname": "小橘的家长",
        # 明文密码：123456（仅用于 mock 联调）
        "password_hash": "$2b$12$LzqZLlN.Q/hxn2pSqlTJ7exGycjfLc.rzfE/N.jL/ZgbpjSJdzXcK",
        "avatar": "https://placehold.co/80x80",
        "password_version": 1,
        "created_at": _now - timedelta(days=10),
        "updated_at": _now - timedelta(days=1),
        **COMMON,
    },
    {
        "id": 2,
        "username": "petlover02",
        "nickname": "阿福主人",
        "password_hash": "$2b$12$LzqZLlN.Q/hxn2pSqlTJ7exGycjfLc.rzfE/N.jL/ZgbpjSJdzXcK",
        "avatar": "https://placehold.co/80x80",
        "password_version": 1,
        "created_at": _now - timedelta(days=8),
        "updated_at": _now - timedelta(days=1),
        **COMMON,
    },
]

POSTS = [
    {
        "id": 1,
        "user_id": 1,
        "title": "萌宠日常第1天",
        "content": "今天带毛孩子去公园玩耍，记录第1天。",
        "images": ["https://placehold.co/800x600?text=pet1"],
        "cover_image": "https://placehold.co/800x600?text=pet1",
        "cover_thumb_url": "https://placehold.co/400x300?text=pet1",
        "like_count": 1,
        "collect_count": 0,
        "comment_count": 4,
        "created_at": _now - timedelta(days=5),
        "updated_at": _now - timedelta(days=5),
        "created_by": 1,
        "updated_by": 1,
        "is_deleted": 0,
    },
    {
        "id": 2,
        "user_id": 2,
        "title": "萌宠日常第2天",
        "content": "今天带毛孩子去公园玩耍，记录第2天。",
        "images": ["https://placehold.co/800x600?text=pet2"],
        "cover_image": "https://placehold.co/800x600?text=pet2",
        "cover_thumb_url": "https://placehold.co/400x300?text=pet2",
        "like_count": 2,
        "collect_count": 1,
        "comment_count": 0,
        "created_at": _now - timedelta(days=4),
        "updated_at": _now - timedelta(days=4),
        "created_by": 2,
        "updated_by": 2,
        "is_deleted": 0,
    },
    {
        "id": 3,
        "user_id": 1,
        "title": "萌宠日常第3天",
        "content": "今天带毛孩子去公园玩耍，记录第3天。",
        "images": ["https://placehold.co/800x600?text=pet3"],
        "cover_image": "https://placehold.co/800x600?text=pet3",
        "cover_thumb_url": "https://placehold.co/400x300?text=pet3",
        "like_count": 3,
        "collect_count": 1,
        "comment_count": 0,
        "created_at": _now - timedelta(days=3),
        "updated_at": _now - timedelta(days=3),
        "created_by": 1,
        "updated_by": 1,
        "is_deleted": 0,
    },
    {
        "id": 4,
        "user_id": 2,
        "title": "萌宠日常第4天",
        "content": "今天带毛孩子去公园玩耍，记录第4天。",
        "images": ["https://placehold.co/800x600?text=pet4"],
        "cover_image": "https://placehold.co/800x600?text=pet4",
        "cover_thumb_url": "https://placehold.co/400x300?text=pet4",
        "like_count": 4,
        "collect_count": 2,
        "comment_count": 0,
        "created_at": _now - timedelta(days=2),
        "updated_at": _now - timedelta(days=2),
        "created_by": 2,
        "updated_by": 2,
        "is_deleted": 0,
    },
    {
        "id": 5,
        "user_id": 1,
        "title": "萌宠日常第5天",
        "content": "今天带毛孩子去公园玩耍，记录第5天。",
        "images": ["https://placehold.co/800x600?text=pet5"],
        "cover_image": "https://placehold.co/800x600?text=pet5",
        "cover_thumb_url": "https://placehold.co/400x300?text=pet5",
        "like_count": 5,
        "collect_count": 2,
        "comment_count": 0,
        "created_at": _now - timedelta(days=1),
        "updated_at": _now - timedelta(days=1),
        "created_by": 1,
        "updated_by": 1,
        "is_deleted": 0,
    },
]

COMMENTS = [
    {
        "id": 1,
        "post_id": 1,
        "user_id": 2,
        "content": "太可爱了！",
        "reply_to_comment_id": None,
        "is_edited": 0,
        "edited_at": None,
        "like_count": 2,
        "reply_count": 2,
        "created_at": _now - timedelta(hours=5),
        "updated_at": _now - timedelta(hours=5),
        "created_by": 2,
        "updated_by": 2,
        "is_deleted": 0,
    },
    {
        "id": 2,
        "post_id": 1,
        "user_id": 1,
        "content": "谢谢喜欢！",
        "reply_to_comment_id": 1,
        "is_edited": 0,
        "edited_at": None,
        "like_count": 1,
        "reply_count": 1,
        "created_at": _now - timedelta(hours=4),
        "updated_at": _now - timedelta(hours=4),
        "created_by": 1,
        "updated_by": 1,
        "is_deleted": 0,
    },
    {
        "id": 3,
        "post_id": 1,
        "user_id": 2,
        "content": "我家毛孩子也爱去这个公园",
        "reply_to_comment_id": 1,
        "is_edited": 0,
        "edited_at": None,
        "like_count": 0,
        "reply_count": 0,
        "created_at": _now - timedelta(hours=3),
        "updated_at": _now - timedelta(hours=3),
        "created_by": 2,
        "updated_by": 2,
        "is_deleted": 0,
    },
    {
        "id": 4,
        "post_id": 1,
        "user_id": 1,
        "content": "哈哈，是呀！它们玩得特别开心",
        "reply_to_comment_id": 2,
        "is_edited": 1,
        "edited_at": _now - timedelta(hours=2),
        "like_count": 0,
        "reply_count": 0,
        "created_at": _now - timedelta(hours=3),
        "updated_at": _now - timedelta(hours=2),
        "created_by": 1,
        "updated_by": 1,
        "is_deleted": 0,
    },
]

COMMENT_LIKES = [
    {
        "id": 1,
        "comment_id": 1,
        "user_id": 1,
        "created_at": _now - timedelta(hours=4),
        "updated_at": _now - timedelta(hours=4),
        "created_by": 1,
        "updated_by": 1,
        "is_deleted": 0,
    },
    {
        "id": 2,
        "comment_id": 1,
        "user_id": 2,
        "created_at": _now - timedelta(hours=3),
        "updated_at": _now - timedelta(hours=3),
        "created_by": 2,
        "updated_by": 2,
        "is_deleted": 0,
    },
    {
        "id": 3,
        "comment_id": 2,
        "user_id": 2,
        "created_at": _now - timedelta(hours=3),
        "updated_at": _now - timedelta(hours=3),
        "created_by": 2,
        "updated_by": 2,
        "is_deleted": 0,
    },
]

LIKES = [
    {"id": 1, "post_id": 1, "user_id": 2, "created_at": _now, "updated_at": _now, "created_by": 2, "updated_by": 2, "is_deleted": 0}
]
COLLECTS = [
    {"id": 1, "post_id": 1, "user_id": 2, "created_at": _now, "updated_at": _now, "created_by": 2, "updated_by": 2, "is_deleted": 0}
]

FORTUNES = [
    {"id": 1, "level": "上上签", "content": "今日与毛孩子贴贴，幸福翻倍。", "day_index": 1, "created_at": _now, "updated_at": _now, **COMMON},
    {"id": 2, "level": "上签", "content": "遛弯会遇到好心情，顺风顺水。", "day_index": 2, "created_at": _now, "updated_at": _now, **COMMON},
    {"id": 3, "level": "中上签", "content": "陪伴就是最好的礼物。", "day_index": 3, "created_at": _now, "updated_at": _now, **COMMON},
    {"id": 4, "level": "中签", "content": "慢慢来，今天也会有小确幸。", "day_index": 4, "created_at": _now, "updated_at": _now, **COMMON},
    {"id": 5, "level": "上签", "content": "新玩具会让主子超开心。", "day_index": 5, "created_at": _now, "updated_at": _now, **COMMON},
    {"id": 6, "level": "中上签", "content": "认真梳毛，福气加倍。", "day_index": 6, "created_at": _now, "updated_at": _now, **COMMON},
    {"id": 7, "level": "上上签", "content": "被小爪爪踩奶，幸运满格。", "day_index": 7, "created_at": _now, "updated_at": _now, **COMMON},
]

CHECKINS = []
NOTIFICATIONS = [
    {
        "id": 1,
        "user_id": 1,
        "type": "comment",
        "content": "阿福主人 评论了你的帖子：太可爱了！",
        "related_id": 1,
        "is_read": False,
        "created_at": _now - timedelta(hours=4),
        "updated_at": _now - timedelta(hours=4),
        "created_by": 0,
        "updated_by": 0,
        "is_deleted": 0,
    }
]
POINTS = [
    {"id": 1, "user_id": 1, "total_points": 40, "created_at": _now, "updated_at": _now, "created_by": 1, "updated_by": 1, "is_deleted": 0},
    {"id": 2, "user_id": 2, "total_points": 20, "created_at": _now, "updated_at": _now, "created_by": 2, "updated_by": 2, "is_deleted": 0},
]
POINTS_LOGS = []
FOLLOWS = []


ID_COUNTER = {
    "users": 3,
    "posts": 6,
    "comments": 5,
    "comment_likes": 4,
    "likes": 2,
    "collects": 2,
    "checkins": 1,
    "notifications": 2,
    "points_logs": 1,
    "follows": 1,
}


def snapshot() -> dict:
    return {
        "users": deepcopy(USERS),
        "posts": deepcopy(POSTS),
        "comments": deepcopy(COMMENTS),
        "comment_likes": deepcopy(COMMENT_LIKES),
        "likes": deepcopy(LIKES),
        "collects": deepcopy(COLLECTS),
        "checkins": deepcopy(CHECKINS),
        "notifications": deepcopy(NOTIFICATIONS),
        "fortunes": deepcopy(FORTUNES),
        "points": deepcopy(POINTS),
        "points_logs": deepcopy(POINTS_LOGS),
        "follows": deepcopy(FOLLOWS),
    }
