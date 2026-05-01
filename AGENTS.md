# 宠光（PetGlow）项目规范文档

> 本文档用于规范 AI 辅助开发时的架构理解、目录结构、编码约定。所有 AI 生成代码必须严格遵守本文档。

---

## 项目概述

**宠光（PetGlow）** 是一个宠物社区微信小程序，核心功能：发布宠物帖子、浏览互动、每日摇签签到、积分系统。

| 层 | 技术栈 |
|----|--------|
| 前端 | uni-app + Vue3 Composition API（编译微信小程序） |
| 后端 | Python 3.11+ / FastAPI / Uvicorn |
| 数据库 | MySQL 8.0（SQLAlchemy ORM，同步模式） |
| 认证 | JWT（python-jose），Token 有效期 7 天 |
| 部署 | Nginx + Uvicorn 单进程 + Supervisor（2核2G 服务器） |

---

## 后端目录结构

```
backend/
├── app/
│   ├── main.py                  # FastAPI 应用入口，注册路由、中间件
│   ├── core/
│   │   ├── config.py            # 环境变量配置（pydantic BaseSettings）
│   │   ├── deps.py              # 依赖注入工厂（get_current_user、get_repo 等）
│   │   ├── security.py          # JWT 生成与校验
│   │   └── response.py          # 统一响应格式工具函数
│   ├── routers/                 # 路由层（仅做参数接收和响应返回，不含业务逻辑）
│   │   ├── auth.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   ├── interactions.py      # 点赞、收藏
│   │   ├── checkin.py
│   │   ├── points.py
│   │   ├── notifications.py
│   │   ├── upload.py
│   │   └── users.py
│   ├── services/                # 业务逻辑层（所有业务规则在此处理）
│   │   ├── auth_service.py
│   │   ├── post_service.py
│   │   ├── comment_service.py
│   │   ├── interaction_service.py
│   │   ├── checkin_service.py
│   │   ├── points_service.py
│   │   ├── notification_service.py
│   │   └── upload_service.py
│   ├── repositories/            # 数据访问层（Repository 模式）
│   │   ├── base.py              # 抽象接口（ABC），定义所有数据操作方法
│   │   ├── mock/                # Mock 实现（USE_MOCK_DB=true 时使用）
│   │   │   ├── mock_data.py     # 内存预置测试数据
│   │   │   ├── user_repo.py
│   │   │   ├── post_repo.py
│   │   │   ├── comment_repo.py
│   │   │   ├── interaction_repo.py
│   │   │   ├── checkin_repo.py
│   │   │   ├── points_repo.py
│   │   │   └── notification_repo.py
│   │   └── db/                  # 真实数据库实现（USE_MOCK_DB=false 时使用）
│   │       ├── user_repo.py
│   │       ├── post_repo.py
│   │       └── ...
│   ├── models/                  # SQLAlchemy ORM 模型（对应数据库表）
│   │   ├── base.py              # BaseModel（含公共字段：created_at/updated_at/created_by/updated_by/is_deleted）
│   │   ├── user.py              # PetUser → pet_user 表
│   │   ├── post.py              # PetPost → pet_post 表
│   │   ├── comment.py
│   │   ├── interaction.py       # PetLike / PetCollect
│   │   ├── checkin.py
│   │   ├── points.py            # PetPoints / PetPointsLog
│   │   ├── notification.py
│   │   └── fortune.py           # PetFortune（好运签池）
│   ├── schemas/                 # Pydantic 数据传输对象（DTO）
│   │   ├── common.py            # 统一响应 Schema、分页 Schema
│   │   ├── auth.py              # LoginReq / RegisterReq / TokenResp / UserInfoResp
│   │   ├── post.py              # PostCreateReq / PostListResp / PostDetailResp
│   │   ├── comment.py           # CommentCreateReq / CommentResp
│   │   ├── interaction.py       # LikeResp / CollectResp
│   │   ├── checkin.py           # CheckinResp / CheckinStatusResp
│   │   ├── points.py            # PointsResp / PointsLogResp
│   │   ├── notification.py      # NotificationResp / UnreadCountResp
│   │   ├── upload.py            # UploadResp
│   │   └── user.py              # UpdateNicknameReq / UpdatePasswordReq / UserProfileResp
│   └── utils/
│       ├── image.py             # 图片压缩、缩略图生成（Pillow）
│       ├── idempotency.py       # 幂等校验（client_id 缓存）
│       └── pagination.py        # 分页工具函数
├── uploads/
│   ├── original/                # 原图（压缩后，长边≤1920px）
│   └── thumb/                   # 缩略图（长边≤400px）
├── sql/
│   └── init.sql                 # 数据库初始化 SQL（建表脚本）
├── .env                         # 环境变量（不提交 git）
├── .env.example                 # 环境变量示例
└── requirements.txt
```

---

## 前端目录结构

```
frontend/
├── src/
│   ├── pages/                   # 页面（对应 pages.json 路由）
│   │   ├── index/               # 首页（瀑布流帖子列表）
│   │   ├── login/               # 登录页
│   │   ├── register/            # 注册页
│   │   ├── post-detail/         # 帖子详情页
│   │   ├── post-publish/        # 发布帖子页
│   │   ├── search/              # 搜索页
│   │   ├── profile/             # 我的页面
│   │   ├── my-posts/            # 我的发布
│   │   ├── my-collects/         # 我的收藏
│   │   ├── my-likes/            # 赞过
│   │   ├── messages/            # 消息页
│   │   ├── settings/            # 设置页
│   │   ├── checkin/             # 摇签签到页
│   │   └── points/              # 积分页
│   ├── components/              # 公共组件
│   │   ├── PostCard.vue         # 帖子卡片（列表用）
│   │   ├── Avatar.vue           # 头像组件
│   │   ├── NavBar.vue           # 顶部导航栏
│   │   ├── Loading.vue          # 加载状态
│   │   ├── Empty.vue            # 空状态
│   │   └── PointsBadge.vue      # 积分徽章
│   ├── composables/             # 可复用逻辑（Composition API）
│   │   ├── useButtonLock.js     # 防二次点击：请求期间锁定按钮
│   │   ├── useRequest.js        # 封装请求，含 pendingRequests 防重
│   │   └── usePagination.js     # 分页加载逻辑
│   ├── stores/                  # Pinia 状态管理
│   │   ├── user.js              # 用户信息、Token
│   │   └── points.js            # 积分总数
│   ├── api/                     # 接口请求函数（按模块拆分）
│   │   ├── request.js           # uni.request 封装基类
│   │   ├── auth.js
│   │   ├── post.js
│   │   ├── comment.js
│   │   ├── checkin.js
│   │   ├── points.js
│   │   ├── notification.js
│   │   └── upload.js
│   ├── utils/
│   │   ├── debounce.js          # 防抖工具（300ms，用于搜索）
│   │   ├── uuid.js              # 生成 client_id（用于幂等）
│   │   └── format.js            # 时间格式化等通用工具
│   └── static/                  # 静态资源（图标、图片）
│       └── tabbar/              # 底部导航萌宠图标
├── pages.json                   # 路由配置
├── manifest.json
└── package.json
```

---

## 接口规范

- **统一前缀**：`/api/v1/`
- **认证**：请求头 `Authorization: Bearer <token>`
- **统一响应格式**：
  ```json
  { "code": 0, "msg": "ok", "data": {} }
  ```
  错误时 `code` 非0，`msg` 为错误描述，`data` 为 `null`
- **分页参数**：`?page=1&page_size=20`，响应 `data` 中含 `total`、`items`
- **图片上传**：`multipart/form-data`，返回 `{ "url": "...", "thumb_url": "..." }`
- **幂等接口**：发帖、评论等创建操作，请求体携带 `client_id`（前端生成 UUID）

---

## 数据库规范

- **表名前缀**：所有表使用 `pet_` 前缀，单数命名（如 `pet_user`，不用 `pet_users`）
- **公共字段**（每张表必须包含）：

  | 字段 | 类型 | 说明 |
  |------|------|------|
  | id | BIGINT AUTO_INCREMENT | 主键 |
  | created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP |
  | updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |
  | created_by | BIGINT | 创建人 id，系统操作填 0 |
  | updated_by | BIGINT | 更新人 id，系统操作填 0 |
  | is_deleted | TINYINT(1) | 0=正常，1=已删除（逻辑删除） |

- **逻辑删除**：所有删除操作执行 `UPDATE ... SET is_deleted=1`，禁止物理删除
- **查询过滤**：所有查询默认加 `WHERE is_deleted=0`

---

## 环境变量（.env）

```
# 应用
APP_SECRET_KEY=your-secret-key
JWT_EXPIRE_DAYS=7

# 数据库（暂无数据库时留空，USE_MOCK_DB=true）
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/furever
USE_MOCK_DB=true

# 文件上传
UPLOAD_DIR=./uploads
STATIC_BASE_URL=http://your-domain/static
```

---

## Mock 数据层说明

当 `USE_MOCK_DB=true` 时，所有数据操作走 `app/repositories/mock/` 下的内存实现，数据在进程重启后重置。切换为 `false` 后自动使用真实数据库，Router 和 Service 层无需任何改动。

---

## 接口文档

完整 OpenAPI 3.0 规范见：[`docs/api/openapi.yaml`](docs/api/openapi.yaml)
