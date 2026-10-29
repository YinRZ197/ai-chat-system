# TECH_DESIGN.md 技术设计文档
## 1. 技术选型
- 前端：Vue3 + Ant Design Vue
- 后端：Python FastAPI
- 数据库：MySQL
- 版本控制：Git，开发分支 dev
- 本地推理：PyTorch 加载pt权重模型，tokenizer与推理脚本放置在model目录
> 说明：pt模型不转换GGUF，不接入Ollama；远端模型通过HTTP调用第三方大模型API

## 2. 数据库设计
### user 用户表
| 字段名 | 类型 | 说明 |
| ---- | ---- | ---- |
| id | int 主键自增 | 用户唯一id |
| username | varchar(50) | 用户名，唯一 |
| password_hash | varchar(255) | bcrypt加密密码 |
| create_time | datetime | 创建时间 |

### model_info 模型信息表
| 字段名 | 类型 | 说明 |
| ---- | ---- | ---- |
| id | int 主键自增 | 模型id |
| model_name | varchar(100) | 模型名称 |
| model_type | varchar(20) | local(本地pt) / remote(远端API) |
| system_prompt | text | 模型专属system提示词 |
| model_path | varchar(200) | 本地模型路径，远端模型为空 |
| create_time | datetime | 添加时间 |

### model_key 远端密钥表
| 字段名 | 类型 | 说明 |
| ---- | ---- | ---- |
| id | int 主键自增 | key编号 |
| model_id | int 外键 | 关联 model_info.id |
| api_key | varchar(255) | 远端API密钥 |
| is_enable | tinyint | 1启用，0禁用 |

### conversation 会话表
| 字段名 | 类型 | 说明 |
| ---- | ---- | ---- |
| id | int 主键自增 | 会话id |
| user_id | int 外键 | 关联 user.id |
| model_id | int 外键 | 本次会话选用模型 |
| title | varchar(100) | 会话标题，支持修改 |
| create_time | datetime | 创建时间 |
| update_time | datetime | 最后更新时间 |

### chat_message 消息表
| 字段名 | 类型 | 说明 |
| ---- | ---- | ---- |
| id | int 主键自增 | 消息id |
| conversation_id | int 外键 | 关联 conversation.id |
| role | varchar(20) | user / assistant |
| content | longtext | 消息内容 |
| create_time | datetime | 发送时间 |

## 3. 项目目录规划
ai-chat-system/
├── model/                # 本地 pt 模型、tokenizer、推理脚本
├── backend/              # FastAPI 后端代码
├── frontend/             # Vue3 + Ant Design Vue 前端
├── PRD.md
├── AGENTS.md
├── TECH_DESIGN.md
└── .gitignore

## 4. 核心接口规划
1. 用户接口：注册、登录
2. 模型管理接口：新增模型、修改system提示词、密钥启用/禁用
3. 会话接口：新建会话、修改标题、删除会话、查询会话列表
4. 聊天接口：发送消息，自动分流：本地pt推理 / 远端API调用

## 5. 部署方案
低配环境：远端API + 本地pt模型
高配环境：远端API + 本地pt模型，可额外增加Ollama模型

## 6. 安全说明
- 用户密码使用bcrypt哈希加密，禁止明文存储
- API密钥加密存放，前端不返回原始密钥

