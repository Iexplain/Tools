# Tools

个人应用集合仓库：用 GitHub Pages 部署的多个 PWA（渐进式网页应用）。用手机 Safari 打开对应链接后「添加到主屏幕」，即可像原生 App 一样全屏使用，支持离线打开，数据保存在手机本地。

## 仓库结构

每个应用一个独立文件夹，互不干扰：

```
仓库根目录/
├── README.md          ← 本文件（仓库说明）
├── qiuzhilu/          ← 求职录（求职面试进度记录）
│   ├── index.html     ← 应用本体（单文件，所有代码内嵌其中）
│   ├── manifest.json  ← PWA 配置（应用名、图标、显示方式）
│   ├── make_icons.py  ← 生成图标的工具脚本
│   ├── sw.js          ← 离线缓存（Service Worker）
│   └── icons/         ← 应用图标（4 个：180 / 192 / 512 / maskable）
└── 以后的新应用       ← 结构同上，见下方「如何添加新应用」
```

## 应用目录

### 1、求职录（qiuzhilu）

求职投递与面试进度记录工具。

**功能：**

- 进度跟踪：已投递 → 筛选中 → 一面 → 二面 → 三面 → HR面 → 已Offer / 被拒 / 拒Offer
- 公司信息：公司、职位、城市、薪资、岗位链接、备注
- 面试提醒：即将到来的面试自动置顶提示（今天 / 明天 / X天后）
- 待办事项：每家公司可添加准备事项并勾选
- 数据备份：导出 CSV（可用 Excel 打开）/ JSON，换手机可导入恢复

**使用：**

1. iPhone 用 Safari 打开 `https://<你的用户名>.github.io/<仓库名>/qiuzhilu/`
2. 点分享按钮 → 「添加到主屏幕」
3. 数据保存在手机本地（localStorage），无需联网，电脑关机不影响使用

## Qucik Start（GitHub Pages）

1. 新建 **Public** 仓库，把本仓库所有文件上传（网页端 Add file → Upload files 即可）
2. 仓库 **Settings → Pages** → Source 选 `Deploy from a branch` → 分支选 `main` → Save
3. 等 1~2 分钟，访问 `https://<你的用户名>.github.io/<仓库名>/qiuzhilu/`

**更新内容**：改完文件重新上传覆盖即可，GitHub 自动更新，手机刷新（或关闭重开）生效。

## 如何添加新应用（重点）

1. 复制 `qiuzhilu/` 的完整文件夹，改名为你的新应用目录名
2. **必改 — 数据钥匙**：打开 `index.html`，搜索 `STORE_KEY`（约第 496 行），把
   `const STORE_KEY = 'interviewTracker.v1';` 改成唯一钥匙，如 `const STORE_KEY = 'notesApp.v1';`
   （同一个仓库多个应用必须用不同钥匙，否则数据会互相覆盖！）
3. **改应用名**：`index.html` 顶部的 `<title>` 和 `<meta name="apple-mobile-web-app-title">`、
   `manifest.json` 里的 `name` / `short_name`
4. **换图标（可选）**：改 `make_icons.py` 里的配色/图形后运行（需 Python + Pillow），
   或在线上传同名的 4 张图标即可
5. 新应用地址：`https://<你的用户名>.github.io/<仓库名>/<新应用目录>/`

## 注意事项

- 文件必须使用**相对路径**（`./index.html`、`icons/...`、`./manifest.json`），这样才能放在子目录下正常部署 —— 现有文件已全部是相对路径，直接复制即可。
- 每个应用目录内必须包含**完整一套**文件（index.html + manifest.json + sw.js + icons/），不能共用。
- `make_icons.py` 是图标生成工具脚本，可根据自己喜欢DIY。
- 更新后手机刷新仍看到旧版时，关闭应用重新打开一次（Service Worker 缓存特性）。
- 数据只在手机本地：删除主屏幕图标 / 清除浏览器网站数据会清空数据，建议定期在应用内「导出数据 → 备份全部数据（JSON）」保存备份。

