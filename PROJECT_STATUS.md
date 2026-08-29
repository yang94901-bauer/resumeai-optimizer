# AI Resume Optimizer - 项目状态（2026-08-29 更新）

## 产品矩阵（Gumroad - 卖家"杨米" yangster4766）
| 产品 | 价格 | URL | product_id | 类型 |
|---|---|---|---|---|
| AI English Resume Optimizer | $9.90 | yangster4766.gumroad.com/l/ai-resume-optimizer | GQ72Bapk2zdvwGrdzKnNQQ== | 网站AI功能 |
| English Job Interview Q&A Template Pack | $4.90 | yangster4766.gumroad.com/l/yojfw | B5Lm25B6KvvlUmkHxBTvZg== | 下载模板 |
| Complete Job Application Bundle | $29.00 | yangster4766.gumroad.com/l/uuqzqb | i91EihlvoR-vVXkMqIRY9Q== | 下载套件 |

## 技术状态
- 主站（AI功能）：https://yang94901.pythonanywhere.com/
- Landing Page（PH用）：https://landing-azure-nine-59.vercel.app/（Vercel部署，resumeai-tool项目）
- 7+ 端点全部 HTTP 200，/api/health 显示 gumroad_configured:true + kimi_configured:true
- 三产品 license 验证通过（POST /v2/licenses/verify）
- 预生成兑换码验证通过（license_codes.txt）
- Kimi API 接入（中文简历→英文简历 AI 生成）
- SEO：4 篇博客 + sitemap + robots

## Product Hunt 发布（已排期 ✅）
- 产品名：ResumeAI
- Tagline：AI English Resume Optimizer - ATS-Ready in 30s
- 发布时间：2026-09-01（周二）PT 午夜（北京时间 9/1 15:01 左右）
- Pre-launch 页面：https://www.producthunt.com/products/resumeai-19/resumeai-23/prelaunch
- 必填项：100% 完成
- 推荐项：Shoutouts ✅ / Video ✅ / First comment ✅ / Categories ✅ / Additional Makers ✅
- Thumbnail + 3 张 Gallery 图片已上传（marketing/producthunt/）

## 服务器密钥文件（PythonAnywhere /home/yang94901/mysite/）
- gumroad_api_key.txt（43 bytes）
- gumroad_product_id.txt（24 bytes）
- gumroad_product_id2.txt（24 bytes）
- gumroad_product_id3.txt（24 bytes）

## 营销状态
- 小红书"涛哥进化论"：7 篇（求职英文简历方向）
- X/Twitter @zeno_lab：6 条（英文获客）
- Gumroad 销售：0 单
- 网站流量：本月 96 次访问
- 定时任务：每日10:30销售+健康监控（已创建）
- 定时任务：PythonAnywhere站点续期 2026-09-20（已创建）

## 关键凭证（勿泄露）
- Gumroad Access Token：i-pId0S7Q13nmrAY4pS5FIns3P-XQm8Z5tGLUass8JE
- Kimi API Key：sk-dTLMiEPMe3zLJhS6TSFBunfcUI9yJJ6pyyrkgccsRIMviwL5
- GitHub：github.com/yang94901-bauer/resumeai-optimizer（public 仓库）
- Vercel 项目：resumeai-tool（已连接GitHub自动部署）

## 待办
- [ ] 9月1日发布日：监控PH排名+回复评论+社交媒体同步
- [ ] 持续营销（小红书/推特每日内容）
- [ ] Codex Pro 订阅利用方案（未落地）
- [ ] 站点每月续期（2026-09-25 前需登录点击续期）
- [ ] 第一单验证端到端转化
- [ ] Landing Page 添加 Product Hunt 徽章
- [ ] 准备发布日社交媒体文案包
