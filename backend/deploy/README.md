# PetGlow 部署说明

## 环境要求
- Python 3.11+
- Nginx
- Supervisor

## 启动步骤
1. `python -m venv .venv`
2. `.\.venv\Scripts\pip install -r requirements.txt`
3. 复制 `.env.example` 为 `.env` 并修改配置
4. `python run.py`（开发）

## 生产部署
1. 使用 `deploy/nginx.conf` 配置反向代理和静态资源
2. 使用 `deploy/supervisor.conf` 托管 Uvicorn 进程
3. 上传目录映射至 `/static/uploads/`
