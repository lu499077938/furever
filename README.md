# 宠光（PetGlow）项目业务与技术说明文档

> 文档版本：v1.0  
> 更新日期：2026-05-01

---

## 一、项目概述

### 1.1 项目定位

**宠光（PetGlow）** 是一款面向宠物爱好者的社区类微信小程序，旨在为用户提供一个分享宠物日常、互动交流、趣味签到的平台。

### 1.2 核心功能

| 功能模块 | 描述 |
|---------|------|
| 帖子发布 | 发布宠物图文内容，支持多图上传 |
| 浏览互动 | 瀑布流浏览帖子，点赞、收藏、评论 |
| 摇签签到 | 每日签到获取随机好运签，赚取积分 |
| 积分系统 | 积分获取与消费，记录积分流水 |
| 用户中心 | 个人资料管理，我的发布/收藏/点赞 |
| 消息通知 | 系统通知，互动消息提醒 |
| 关注系统 | 关注/取消关注用户，查看关注列表 |

### 1.3 技术架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                      微信小程序端                            │
│              uni-app + Vue3 Composition API                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      后端服务层                              │
│              Python 3.11+ / FastAPI / Uvicorn               │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ SQLAlchemy ORM
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      数据存储层                              │
│                    MySQL 8.0                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、技术栈详解

### 2.1 前端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| uni-app | - | 跨平台小程序开发框架 |
| Vue 3 | - | 渐进式 JavaScript 框架 |
| Composition API | - | Vue 3 组合式 API |
| Pinia | - | 状态管理 |
| uni.request | - | 网络请求封装 |

**前端特性：**
- 编译为微信小程序原生代码
- 使用 Composition API 组织代码逻辑
- Pinia 管理全局状态（用户信息、积分等）
- 自定义 composables 实现逻辑复用

### 2.2 后端技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 后端开发语言 |
| FastAPI | - | 高性能 Web 框架 |
| Uvicorn | - | ASGI 服务器 |
| SQLAlchemy | - | ORM 框架（同步模式） |
| PyMySQL | - | MySQL 驱动 |
| python-jose | - | JWT 令牌处理 |
| bcrypt | - | 密码加密 |
| Pydantic | - | 数据验证与序列化 |
| Pillow | - | 图片处理 |

### 2.3 数据库

| 技术 | 版本 | 用途 |
|------|------|------|
| MySQL | 8.0 | 关系型数据库 |

### 2.4 部署架构

| 组件 | 用途 |
|------|------|
| Nginx | 反向代理、静态资源服务 |
| Uvicorn | ASGI 应用服务器 |
| Supervisor | 进程管理守护 |

---

## 三、快速开始

### 3.1 环境要求

| 环境 | 版本要求 |
|------|---------|
| Python | 3.11+ |
| Node.js | 16+ |
| MySQL | 8.0+ |
| npm/pnpm | 最新稳定版 |

### 3.2 后端启动

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境（推荐）
python -m venv venv

# Windows 激活虚拟环境
venv\Scripts\activate

# Linux/Mac 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
# 复制环境变量示例文件
copy .env.example .env    # Windows
cp .env.example .env      # Linux/Mac

# 编辑 .env 文件，配置数据库连接等参数

# 5. 启动开发服务器
python run.py

# 或使用 uvicorn 直接启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**后端服务启动后：**
- API 地址：http://localhost:8000
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/api/v1/health

### 3.3 前端启动

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install
# 或使用 pnpm
pnpm install

# 3. 开发模式启动

# H5 开发模式
npm run dev:h5

# 微信小程序开发模式
npm run dev:mp-weixin

# 4. 构建生产版本

# 构建 H5 版本
npm run build:h5

# 构建微信小程序版本
npm run build:mp-weixin
```

**前端开发说明：**
- H5 开发模式启动后，在浏览器打开 http://localhost:5173
- 微信小程序开发模式启动后，使用微信开发者工具打开 `dist/dev/mp-weixin` 目录

### 3.4 数据库初始化

```bash
# 1. 创建数据库
mysql -u root -p
CREATE DATABASE furever DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 2. 执行初始化脚本
mysql -u root -p furever < backend/sql/init.sql

# 3. 修改 .env 配置
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/furever
USE_MOCK_DB=false
```

### 3.5 Mock 模式开发

项目支持 Mock 数据模式，无需配置数据库即可快速启动开发：

```bash
# 在 .env 中设置
USE_MOCK_DB=true
```

Mock 模式下，所有数据操作在内存中进行，适合快速开发和测试。

---

## 四、后端架构设计

### 4.1 分层架构

后端采用经典的四层架构设计：

```
┌─────────────────────────────────────────────────────────────┐
│                    Routers 路由层                            │
│         接收请求、参数校验、调用服务、返回响应                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Services 业务层                            │
│              业务逻辑处理、事务控制、数据组装                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Repositories 数据层                          │
│              数据访问抽象、CRUD 操作封装                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Models 模型层                              │
│              数据库表映射、ORM 模型定义                        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 目录结构

```
backend/
├── app/
│   ├── main.py                  # FastAPI 应用入口
│   ├── core/                    # 核心模块
│   │   ├── config.py            # 配置管理（环境变量）
│   │   ├── deps.py              # 依赖注入工厂
│   │   ├── security.py          # JWT 生成与校验
│   │   └── response.py          # 统一响应格式
│   ├── routers/                 # 路由层（11个模块）
│   │   ├── auth.py              # 认证：注册、登录
│   │   ├── users.py             # 用户：资料管理
│   │   ├── posts.py             # 帖子：发布、列表、详情
│   │   ├── comments.py          # 评论：发布、回复、点赞
│   │   ├── interactions.py      # 互动：点赞、收藏
│   │   ├── checkin.py           # 签到：摇签、状态
│   │   ├── points.py            # 积分：总览、流水
│   │   ├── notifications.py     # 通知：列表、已读
│   │   ├── follow.py            # 关注：关注/取关
│   │   ├── upload.py            # 上传：图片上传
│   │   └── health.py            # 健康检查
│   ├── services/                # 业务层（11个服务）
│   │   ├── auth_service.py      # 认证服务
│   │   ├── user_service.py      # 用户服务
│   │   ├── post_service.py      # 帖子服务
│   │   ├── comment_service.py   # 评论服务
│   │   ├── interaction_service.py # 互动服务
│   │   ├── checkin_service.py   # 签到服务
│   │   ├── points_service.py    # 积分服务
│   │   ├── notification_service.py # 通知服务
│   │   ├── follow_service.py    # 关注服务
│   │   ├── upload_service.py    # 上传服务
│   │   └── profile_service.py   # 个人中心服务
│   ├── repositories/            # 数据访问层
│   │   ├── base.py              # 抽象接口定义
│   │   └── mock/                # Mock 实现（开发测试）
│   │       ├── mock_data.py     # 内存测试数据
│   │       └── *_repo.py        # 各模块 Mock 实现
│   ├── models/                  # ORM 模型
│   │   └── schemas.py           # 数据库表定义
│   ├── schemas/                 # Pydantic DTO
│   │   ├── common.py            # 通用响应结构
│   │   ├── auth.py              # 认证相关 DTO
│   │   ├── user.py              # 用户相关 DTO
│   │   ├── post.py              # 帖子相关 DTO
│   │   ├── comment.py           # 评论相关 DTO
│   │   ├── interaction.py       # 互动相关 DTO
│   │   ├── checkin.py           # 签到相关 DTO
│   │   ├── points.py            # 积分相关 DTO
│   │   ├── notification.py      # 通知相关 DTO
│   │   ├── follow.py            # 关注相关 DTO
│   │   └── upload.py            # 上传相关 DTO
│   └── utils/                   # 工具函数
│       ├── image.py             # 图片处理
│       └── idempotency.py       # 幂等校验
├── uploads/                     # 上传文件存储
│   ├── original/                # 原图
│   └── thumb/                   # 缩略图
├── sql/
│   └── init.sql                 # 数据库初始化脚本
├── .env                         # 环境变量
└── requirements.txt             # Python 依赖
```

### 4.3 依赖注入设计

项目使用 FastAPI 的依赖注入系统实现解耦：

```python
# 核心依赖注入工厂 (core/deps.py)

# Repository 工厂函数
def get_user_repo() -> UserRepository
def get_post_repo() -> PostRepository
def get_comment_repo() -> CommentRepository
def get_interaction_repo() -> InteractionRepository
def get_checkin_repo() -> CheckinRepository
def get_points_repo() -> PointsRepository
def get_notification_repo() -> NotificationRepository
def get_profile_repo() -> ProfileRepository
def get_follow_repo() -> FollowRepository

# 认证依赖
def get_current_user() -> dict          # 必须登录
def get_current_user_optional() -> dict | None  # 可选登录
```

### 4.4 Repository 模式

通过抽象接口实现数据层解耦，支持 Mock 和真实数据库切换：

```python
# repositories/base.py - 抽象接口
class UserRepository(ABC):
    @abstractmethod
    def create(self, username: str, password_hash: str, nickname: str) -> dict: ...
    
    @abstractmethod
    def get_by_username(self, username: str) -> dict | None: ...
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> dict | None: ...

# repositories/mock/user_repo.py - Mock 实现
class MockUserRepository(UserRepository):
    # 使用内存字典存储，适合开发测试

# repositories/db/user_repo.py - 数据库实现（待开发）
class DbUserRepository(UserRepository):
    # 使用 SQLAlchemy 操作真实数据库
```

**切换方式：** 通过环境变量 `USE_MOCK_DB=true/false` 控制

---

## 五、数据库设计

### 5.1 表结构概览

| 表名 | 描述 | 核心字段 |
|------|------|---------|
| pet_user | 用户表 | id, username, nickname, password_hash, avatar |
| pet_post | 帖子表 | id, user_id, title, content, images, like_count |
| pet_comment | 评论表 | id, post_id, user_id, content |
| pet_like | 点赞表 | id, user_id, post_id |
| pet_collect | 收藏表 | id, user_id, post_id |
| pet_fortune | 好运签池 | id, level, content, day_index |
| pet_checkin | 签到记录 | id, user_id, checkin_date, fortune_id, points_earned |
| pet_notification | 通知表 | id, user_id, type, content, is_read |
| pet_points | 积分表 | id, user_id, total_points |
| pet_points_log | 积分流水 | id, user_id, source, amount, remark |

### 5.2 公共字段规范

所有表必须包含以下公共字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键，自增 |
| created_at | DATETIME | 创建时间，默认当前时间 |
| updated_at | DATETIME | 更新时间，自动更新 |
| created_by | BIGINT | 创建人 ID，系统操作填 0 |
| updated_by | BIGINT | 更新人 ID，系统操作填 0 |
| is_deleted | TINYINT(1) | 逻辑删除标记，0=正常，1=已删除 |

### 5.3 表结构详情

#### 5.3.1 用户表 (pet_user)

```sql
CREATE TABLE pet_user (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(20) NOT NULL UNIQUE,      -- 登录用户名
  nickname VARCHAR(20) NOT NULL,              -- 昵称
  password_hash VARCHAR(255) NOT NULL,        -- 密码哈希
  avatar VARCHAR(255) DEFAULT '',             -- 头像URL
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0
);
```

#### 5.3.2 帖子表 (pet_post)

```sql
CREATE TABLE pet_post (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,                    -- 发布者ID
  title VARCHAR(50) NOT NULL,                 -- 标题
  content VARCHAR(500) NOT NULL,              -- 内容
  cover_image VARCHAR(255) NOT NULL,          -- 封面图URL
  cover_thumb_url VARCHAR(255) NOT NULL,      -- 封面缩略图URL
  images JSON NOT NULL,                       -- 图片列表JSON
  like_count INT DEFAULT 0,                   -- 点赞数
  collect_count INT DEFAULT 0,                -- 收藏数
  comment_count INT DEFAULT 0,                -- 评论数
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0
);
```

#### 5.3.3 评论表 (pet_comment)

```sql
CREATE TABLE pet_comment (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  post_id BIGINT NOT NULL,                    -- 帖子ID
  user_id BIGINT NOT NULL,                    -- 评论者ID
  content VARCHAR(200) NOT NULL,              -- 评论内容
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0
);
```

#### 5.3.4 点赞表 (pet_like)

```sql
CREATE TABLE pet_like (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  post_id BIGINT NOT NULL,
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0,
  UNIQUE KEY uk_user_post_like (user_id, post_id, is_deleted)  -- 联合唯一索引
);
```

#### 5.3.5 收藏表 (pet_collect)

```sql
CREATE TABLE pet_collect (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  post_id BIGINT NOT NULL,
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0,
  UNIQUE KEY uk_user_post_collect (user_id, post_id, is_deleted)
);
```

#### 5.3.6 好运签池表 (pet_fortune)

```sql
CREATE TABLE pet_fortune (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  level VARCHAR(20) NOT NULL,                 -- 签等级（上上签、上签等）
  content VARCHAR(255) NOT NULL,              -- 签文内容
  day_index TINYINT DEFAULT 0,                -- 日期索引
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0
);
```

#### 5.3.7 签到记录表 (pet_checkin)

```sql
CREATE TABLE pet_checkin (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  checkin_date DATE NOT NULL,                 -- 签到日期
  fortune_id BIGINT NOT NULL,                 -- 抽到的签ID
  points_earned INT DEFAULT 0,                -- 获得积分
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0,
  UNIQUE KEY uk_user_checkin (user_id, checkin_date, is_deleted)  -- 每日唯一签到
);
```

#### 5.3.8 通知表 (pet_notification)

```sql
CREATE TABLE pet_notification (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,                    -- 接收者ID
  type VARCHAR(30) NOT NULL,                  -- 通知类型
  content VARCHAR(255) NOT NULL,              -- 通知内容
  related_id BIGINT DEFAULT 0,                -- 关联ID
  is_read TINYINT(1) DEFAULT 0,               -- 是否已读
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0
);
```

#### 5.3.9 积分表 (pet_points)

```sql
CREATE TABLE pet_points (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL UNIQUE,             -- 用户ID（唯一）
  total_points INT DEFAULT 0,                 -- 总积分
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0
);
```

#### 5.3.10 积分流水表 (pet_points_log)

```sql
CREATE TABLE pet_points_log (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  source VARCHAR(30) NOT NULL,                -- 积分来源
  amount INT NOT NULL,                        -- 积分变动（正负）
  remark VARCHAR(255) DEFAULT '',             -- 备注
  -- 公共字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  created_by BIGINT DEFAULT 0,
  updated_by BIGINT DEFAULT 0,
  is_deleted TINYINT(1) DEFAULT 0
);
```

### 5.4 设计规范

1. **表名规范**：使用 `pet_` 前缀，单数命名
2. **逻辑删除**：所有删除操作设置 `is_deleted=1`，禁止物理删除
3. **查询过滤**：所有查询默认添加 `WHERE is_deleted=0` 条件
4. **索引设计**：
   - 主键使用自增 BIGINT
   - 外键关系字段建立索引
   - 唯一约束使用联合唯一索引

---

## 六、API 接口设计

### 6.1 接口规范

#### 6.1.1 基础信息

| 项目 | 规范 |
|------|------|
| 基础路径 | `/api/v1` |
| 协议 | HTTP/HTTPS |
| 数据格式 | JSON |
| 编码 | UTF-8 |

#### 6.1.2 认证方式

```
Authorization: Bearer <token>
```

- 使用 JWT 令牌认证
- Token 有效期：7 天
- Token 中包含用户 ID 和密码版本号

#### 6.1.3 统一响应格式

**成功响应：**
```json
{
  "code": 0,
  "msg": "ok",
  "data": { ... }
}
```

**失败响应：**
```json
{
  "code": 1,
  "msg": "错误描述",
  "data": null
}
```

#### 6.1.4 分页参数

```
GET /api/v1/posts?page=1&page_size=20
```

**分页响应：**
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "total": 100,
    "items": [...]
  }
}
```

### 6.2 接口列表

#### 6.2.1 认证模块 (/auth)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | /auth/register | 用户注册 | 否 |
| POST | /auth/login | 用户登录 | 否 |

**注册请求：**
```json
{
  "username": "string",    // 3-20字符
  "password": "string",    // 6-20字符
  "nickname": "string"     // 1-20字符
}
```

**登录请求：**
```json
{
  "username": "string",
  "password": "string"
}
```

**登录响应：**
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": 1,
      "username": "test",
      "nickname": "测试用户",
      "avatar": ""
    }
  }
}
```

#### 6.2.2 用户模块 (/users)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /users/me | 获取当前用户信息 | 是 |
| PUT | /users/me/nickname | 修改昵称 | 是 |
| PUT | /users/me/avatar | 修改头像 | 是 |
| PUT | /users/me/password | 修改密码 | 是 |
| GET | /users/me/posts | 我的发布 | 是 |
| GET | /users/me/collects | 我的收藏 | 是 |
| GET | /users/me/likes | 我的点赞 | 是 |
| POST | /users/{target_user_id}/follow | 关注/取关用户 | 是 |

#### 6.2.3 帖子模块 (/posts)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | /posts | 发布帖子 | 是 |
| GET | /posts | 帖子列表 | 否 |
| GET | /posts/search | 搜索帖子 | 否 |
| GET | /posts/{post_id} | 帖子详情 | 可选 |
| DELETE | /posts/{post_id} | 删除帖子 | 是 |

**发布帖子请求：**
```json
{
  "title": "string",       // 1-50字符
  "content": "string",     // 1-500字符
  "images": ["url1", "url2"],
  "client_id": "uuid"      // 幂等性保证
}
```

#### 6.2.4 评论模块 (/posts/{post_id}/comments)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | /posts/{post_id}/comments | 发表评论 | 是 |
| GET | /posts/{post_id}/comments | 评论列表 | 否 |
| PUT | /posts/{post_id}/comments/{comment_id} | 修改评论 | 是 |
| DELETE | /posts/{post_id}/comments/{comment_id} | 删除评论 | 是 |
| POST | /posts/{post_id}/comments/{comment_id}/reply | 回复评论 | 是 |
| GET | /posts/{post_id}/comments/{comment_id}/replies | 回复列表 | 否 |
| POST | /posts/{post_id}/comments/{comment_id}/like | 点赞评论 | 是 |
| GET | /posts/{post_id}/comments/{comment_id}/likes | 点赞用户列表 | 否 |

#### 6.2.5 互动模块 (/posts/{post_id})

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | /posts/{post_id}/like | 点赞/取消点赞 | 是 |
| POST | /posts/{post_id}/collect | 收藏/取消收藏 | 是 |

#### 6.2.6 签到模块 (/checkin)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | /checkin | 每日签到 | 是 |
| GET | /checkin/status | 签到状态 | 是 |

**签到响应：**
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "fortune": {
      "level": "上上签",
      "content": "今日运势..."
    },
    "points_earned": 10,
    "continuous_days": 5
  }
}
```

#### 6.2.7 积分模块 (/points)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /points | 积分总览 | 是 |
| GET | /points/logs | 积分流水 | 是 |

#### 6.2.8 通知模块 (/notifications)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /notifications | 通知列表 | 是 |
| GET | /notifications/unread-count | 未读数量 | 是 |
| PUT | /notifications/read-all | 全部已读 | 是 |
| PUT | /notifications/{id}/read | 标记已读 | 是 |

#### 6.2.9 上传模块 (/upload)

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| POST | /upload/image | 上传图片 | 是 |

**上传响应：**
```json
{
  "code": 0,
  "msg": "ok",
  "data": {
    "url": "http://xxx/original/xxx.jpg",
    "thumb_url": "http://xxx/thumb/xxx.jpg"
  }
}
```

#### 6.2.10 健康检查

| 方法 | 路径 | 描述 | 认证 |
|------|------|------|------|
| GET | /health | 服务健康检查 | 否 |

---

## 七、前端架构设计

### 7.1 目录结构

```
frontend/
├── src/
│   ├── pages/                   # 页面（16个页面）
│   │   ├── index/               # 首页（帖子瀑布流）
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
│   │   │   ├── edit-nickname/   # 修改昵称
│   │   │   └── edit-password/   # 修改密码
│   │   ├── checkin/             # 摇签签到页
│   │   └── points/              # 积分中心
│   ├── components/              # 公共组件
│   ├── composables/             # 组合式函数
│   │   ├── useButtonLock.js     # 防二次点击
│   │   ├── useRequest.js        # 请求封装
│   │   └── usePagination.js     # 分页逻辑
│   ├── stores/                  # Pinia 状态管理
│   │   ├── user.js              # 用户状态
│   │   └── points.js            # 积分状态
│   ├── api/                     # API 请求模块
│   │   ├── request.js           # 基础请求封装
│   │   ├── auth.js              # 认证 API
│   │   ├── user.js              # 用户 API
│   │   ├── post.js              # 帖子 API
│   │   ├── comment.js           # 评论 API
│   │   ├── interaction.js       # 互动 API
│   │   ├── checkin.js           # 签到 API
│   │   ├── points.js            # 积分 API
│   │   ├── notification.js      # 通知 API
│   │   ├── follow.js            # 关注 API
│   │   └── upload.js            # 上传 API
│   ├── utils/                   # 工具函数
│   │   ├── debounce.js          # 防抖
│   │   ├── uuid.js              # UUID 生成
│   │   └── format.js            # 格式化工具
│   └── static/                  # 静态资源
│       └── tabbar/              # 底部导航图标
├── pages.json                   # 路由配置
├── manifest.json                # 应用配置
└── package.json                 # 依赖配置
```

### 7.2 页面路由配置

```json
{
  "pages": [
    { "path": "pages/index/index", "navigationBarTitleText": "宠光" },
    { "path": "pages/post-publish/index", "navigationBarTitleText": "发布" },
    { "path": "pages/profile/index", "navigationBarTitleText": "我的" },
    { "path": "pages/login/index", "navigationBarTitleText": "登录" },
    { "path": "pages/register/index", "navigationBarTitleText": "注册" },
    { "path": "pages/post-detail/index", "navigationBarTitleText": "帖子详情" },
    { "path": "pages/search/index", "navigationBarTitleText": "搜索" },
    { "path": "pages/my-posts/index", "navigationBarTitleText": "我的发布" },
    { "path": "pages/my-collects/index", "navigationBarTitleText": "我的收藏" },
    { "path": "pages/my-likes/index", "navigationBarTitleText": "赞过" },
    { "path": "pages/messages/index", "navigationBarTitleText": "消息" },
    { "path": "pages/settings/index", "navigationBarTitleText": "设置" },
    { "path": "pages/checkin/index", "navigationBarTitleText": "摇签签到" },
    { "path": "pages/points/index", "navigationBarTitleText": "积分中心" }
  ],
  "tabBar": {
    "color": "#7a7e83",
    "selectedColor": "#ff8ab3",
    "list": [
      { "pagePath": "pages/index/index", "text": "首页" },
      { "pagePath": "pages/post-publish/index", "text": "发布" },
      { "pagePath": "pages/profile/index", "text": "我的" }
    ]
  }
}
```

### 7.3 请求封装设计

```javascript
// api/request.js
const BASE_URL = "http://127.0.0.1:8000/api/v1";
const pendingRequests = new Map();

export function apiRequest(options) {
  // 防重复提交
  const key = `${options.method}:${options.url}`;
  if (pendingRequests.has(key)) {
    return Promise.reject(new Error("请求进行中，请勿重复提交"));
  }
  
  pendingRequests.set(key, true);
  const token = uni.getStorageSync("token");
  
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${options.url}`,
      header: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      success: (res) => {
        if (res.data.code !== 0) {
          uni.showToast({ title: res.data.msg, icon: "none" });
          reject(new Error(res.data.msg));
          return;
        }
        resolve(res.data.data);
      },
      fail: (err) => {
        uni.showToast({ title: "网络异常", icon: "none" });
        reject(err);
      },
      complete: () => pendingRequests.delete(key),
    });
  });
}
```

### 7.4 状态管理设计

```javascript
// stores/user.js
export const useUserStore = defineStore('user', {
  state: () => ({
    token: uni.getStorageSync('token') || '',
    userInfo: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    setToken(token) {
      this.token = token;
      uni.setStorageSync('token', token);
    },
    
    logout() {
      this.token = '';
      this.userInfo = null;
      uni.removeStorageSync('token');
    }
  }
});
```

---

## 八、安全设计

### 8.1 密码安全

- 使用 **bcrypt** 进行密码哈希
- 自动加盐，防止彩虹表攻击
- 密码版本机制，修改密码后旧 Token 失效

```python
# 密码加密
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

# 密码验证
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
```

### 8.2 JWT 认证

```python
# Token 生成
def create_access_token(user_id: int, password_version: int = 1) -> str:
    expire_at = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {
        "sub": str(user_id),      # 用户ID
        "pv": password_version,   # 密码版本
        "exp": expire_at          # 过期时间
    }
    return jwt.encode(payload, settings.app_secret_key, algorithm="HS256")

# Token 解码
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.app_secret_key, algorithms=["HS256"])
```

### 8.3 接口安全

1. **认证保护**：敏感接口需要 Token 认证
2. **幂等性保证**：创建操作携带 `client_id` 防重复
3. **参数校验**：使用 Pydantic 进行严格参数验证
4. **请求防重**：前端对相同请求进行去重

### 8.4 图片上传安全

```python
# 文件类型校验
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_upload_file(file: UploadFile, content: bytes):
    # 检查文件大小
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(400, "文件大小超过限制")
    
    # 检查文件扩展名
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "不支持的文件类型")
```

---

## 九、环境配置

### 9.1 环境变量

```bash
# 应用配置
APP_NAME=PetGlow API
APP_SECRET_KEY=your-secret-key-here
JWT_EXPIRE_DAYS=7

# 数据库配置
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/furever
USE_MOCK_DB=true                    # 开发环境使用 Mock 数据

# 文件上传配置
UPLOAD_DIR=./uploads
STATIC_BASE_URL=http://localhost:8000/static/uploads
```

### 9.2 开发环境

```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 8.3 生产部署

```bash
# Nginx 配置示例
server {
    listen 80;
    server_name your-domain.com;
    
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /path/to/uploads/;
    }
}

# Supervisor 配置
[program:petglow]
command=uvicorn app.main:app --host 127.0.0.1 --port 8000
directory=/path/to/backend
autostart=true
autorestart=true
```

---

## 十、技术亮点总结

| 特性 | 说明 |
|------|------|
| 分层架构 | Router → Service → Repository → Model，职责清晰 |
| Repository 模式 | 数据层抽象，支持 Mock/DB 切换，便于测试 |
| JWT 认证 | 无状态认证，支持密码版本控制 |
| 逻辑删除 | 数据安全，支持数据恢复 |
| 统一响应 | 标准化 API 响应格式 |
| 幂等设计 | client_id 防止重复提交 |
| 图片处理 | 自动压缩、缩略图生成 |
| 防重请求 | 前端请求去重机制 |

---

## 十一、附录

### 11.1 完整 API 端点列表

| 模块 | 方法 | 端点 | 描述 |
|------|------|------|------|
| 认证 | POST | /api/v1/auth/register | 用户注册 |
| 认证 | POST | /api/v1/auth/login | 用户登录 |
| 用户 | GET | /api/v1/users/me | 获取当前用户 |
| 用户 | PUT | /api/v1/users/me/nickname | 修改昵称 |
| 用户 | PUT | /api/v1/users/me/avatar | 修改头像 |
| 用户 | PUT | /api/v1/users/me/password | 修改密码 |
| 用户 | GET | /api/v1/users/me/posts | 我的发布 |
| 用户 | GET | /api/v1/users/me/collects | 我的收藏 |
| 用户 | GET | /api/v1/users/me/likes | 我的点赞 |
| 关注 | POST | /api/v1/users/{id}/follow | 关注/取关 |
| 帖子 | POST | /api/v1/posts | 发布帖子 |
| 帖子 | GET | /api/v1/posts | 帖子列表 |
| 帖子 | GET | /api/v1/posts/search | 搜索帖子 |
| 帖子 | GET | /api/v1/posts/{id} | 帖子详情 |
| 帖子 | DELETE | /api/v1/posts/{id} | 删除帖子 |
| 互动 | POST | /api/v1/posts/{id}/like | 点赞/取消 |
| 互动 | POST | /api/v1/posts/{id}/collect | 收藏/取消 |
| 评论 | POST | /api/v1/posts/{id}/comments | 发表评论 |
| 评论 | GET | /api/v1/posts/{id}/comments | 评论列表 |
| 评论 | PUT | /api/v1/posts/{id}/comments/{cid} | 修改评论 |
| 评论 | DELETE | /api/v1/posts/{id}/comments/{cid} | 删除评论 |
| 评论 | POST | /api/v1/posts/{id}/comments/{cid}/reply | 回复评论 |
| 评论 | GET | /api/v1/posts/{id}/comments/{cid}/replies | 回复列表 |
| 评论 | POST | /api/v1/posts/{id}/comments/{cid}/like | 点赞评论 |
| 签到 | POST | /api/v1/checkin | 每日签到 |
| 签到 | GET | /api/v1/checkin/status | 签到状态 |
| 积分 | GET | /api/v1/points | 积分总览 |
| 积分 | GET | /api/v1/points/logs | 积分流水 |
| 通知 | GET | /api/v1/notifications | 通知列表 |
| 通知 | GET | /api/v1/notifications/unread-count | 未读数量 |
| 通知 | PUT | /api/v1/notifications/read-all | 全部已读 |
| 通知 | PUT | /api/v1/notifications/{id}/read | 标记已读 |
| 上传 | POST | /api/v1/upload/image | 上传图片 |
| 健康 | GET | /api/v1/health | 健康检查 |

### 11.2 数据库 ER 关系

```
pet_user ──┬── pet_post ──┬── pet_comment
           │              ├── pet_like
           │              └── pet_collect
           │
           ├── pet_checkin ── pet_fortune
           │
           ├── pet_points
           │   └── pet_points_log
           │
           └── pet_notification
```

---

> 文档结束 | 宠光（PetGlow）项目组
