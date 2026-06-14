# 打字速度测试 - Typing Speed Test

免费在线打字速度测试工具，实时检测 WPM 打字速度和准确率。

## 功能

- 30/60/120 秒三种测试模式
- 实时 WPM 和准确率显示
- 逐字高亮（正确/错误/当前光标）
- 测试结果详细统计
- 响应式设计，支持手机和电脑

## 部署到 Vercel（免费）

### 第一步：安装工具

1. 安装 Git：https://git-scm.com/downloads
2. 安装 Node.js：https://nodejs.org/
3. 注册 Vercel 账号：https://vercel.com（可用 GitHub 登录）

### 第二步：上传到 GitHub

```bash
cd d:\code\typing-test
git init
git add .
git commit -m "Initial commit"
```

然后在 GitHub 上创建一个新仓库，按提示推送代码：

```bash
git remote add origin https://github.com/你的用户名/typing-test.git
git branch -M main
git push -u origin main
```

### 第三步：部署到 Vercel

1. 登录 https://vercel.com
2. 点击 "New Project"
3. 导入你的 GitHub 仓库
4. 点击 Deploy，等待部署完成
5. 你会得到一个 `xxx.vercel.app` 的免费域名

### 第四步：申请 Google AdSense

1. 访问 https://www.google.com/adsense/
2. 添加你的网站域名
3. 等待审核通过（通常几天到几周）
4. 获取你的 AdSense ID（ca-pub-xxx）
5. 在 index.html 中取消广告位注释，替换为你的 ID

### 第五步：SEO 优化

1. 将 index.html 中所有 `your-domain.com` 替换为你的实际域名
2. 在 Google Search Console 提交你的网站
3. 提交 sitemap.xml

## 广告变现说明

- Google AdSense 需要网站有一定流量才会审核通过
- 建议先通过社交媒体、论坛等渠道引流
- 每 1000 次页面浏览大约可获得 $1-$5 的广告收入
- 流量越大，收入越高

## 技术栈

- 纯 HTML/CSS/JavaScript，无依赖
- 可直接部署为静态网站
- 支持 Vercel、GitHub Pages、Netlify 等平台
