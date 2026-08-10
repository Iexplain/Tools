# Tools

个人应用集合仓库：用 GitHub Pages 部署的多个 PWA（渐进式网页应用）。用手机 Safari 打开对应链接后「添加到主屏幕」，即可像原生 App 一样全屏使用，支持离线打开，数据保存在手机本地。

## 仓库结构

每个应用一个独立文件夹，互不干扰：

```
仓库根目录/
├── README.md          ← 本文件（仓库说明）
├── index.html         ← 入口页（自动展示所有应用列表，本身也可添加到主屏幕）
├── manifest.json      ← 入口页的 PWA 配置
├── sw.js              ← 入口页的离线缓存
├── make_icons.py      ← 入口页图标生成脚本
├── icons/             ← 入口页图标（4 个）
├── qiuzhilu/          ← 求职录（求职面试进度记录）
│   ├── index.html     ← 应用本体（单文件，所有代码内嵌其中）
│   ├── manifest.json  ← PWA 配置（应用名、图标、显示方式）
│   ├── make_icons.py  ← 生成图标的工具脚本
│   ├── sw.js          ← 离线缓存（Service Worker）
│   └── icons/         ← 应用图标（4 个：180 / 192 / 512 / maskable）
├── jizhangji/         ← 记账本（收支记账），结构同上
└── 以后的新应用       ← 结构同上，见下方「如何添加新应用」
```

## 应用目录

访问入口：`https://iexplain.github.io/Tools/`（自动展示所有应用列表）

这个入口页本身也是一个 PWA，可以单独「添加到主屏幕」，点一下就能进任意子应用。

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

### 2、记账本（jizhangji）

简洁的收支记账工具，按月切换、分类汇总、本地存储。

**功能：**

- 一笔一笔记账：金额、类型（支出 / 收入）、分类、日期、备注
- 预置分类：支出 8 类（餐饮、交通、购物、居住、医疗、娱乐、学习、其他）+ 收入 6 类（工资、奖金、兼职、投资、红包、其他）
- 月度统计：本月收入 / 支出 / 结余 + 按分类汇总（含百分比进度条）
- 图表：本月分类占比环形图（支出 / 收入可切换）+ 近 6 个月收支柱状图
- 月份切换：左右按钮切换月份查看历史账
- 数据备份：导出 CSV（可用 Excel 打开）/ JSON，换手机可导入恢复

**使用：**

1. iPhone 用 Safari 打开 `https://<你的用户名>.github.io/<仓库名>/jizhangji/`
2. 点分享按钮 → 「添加到主屏幕」
3. 数据保存在手机本地（localStorage），换手机记得先导出 JSON 备份

## Quick Start（GitHub Pages）

1. 新建 **Public** 仓库，把本仓库所有文件上传（网页端 Add file → Upload files 即可）
2. 仓库 **Settings → Pages** → Source 选 `Deploy from a branch` → 分支选 `main` → Save
3. 等 1~2 分钟，访问 `https://<你的用户名>.github.io/<仓库名>/qiuzhilu/`

**更新内容**：改完文件重新上传覆盖即可，GitHub 自动更新，手机刷新即生效（应用本体走「联网优先」，
有网时永远拿到最新版；没网时用上次缓存的版本，照常离线可用）。

## 常见问题

### 打开链接是 404？

说明 GitHub Pages 还没开启（或配置不对），按下面步骤操作一次：

1. 进仓库的 **Settings**（齿轮图标）
2. 左侧菜单找到 **Pages**
3. **Source** 选 `Deploy from a branch`
4. **Branch** 选 `main`、**文件夹**选 `/` (root) → 点 **Save**
5. 等 1~2 分钟，刷新页面，GitHub 会显示绿色横幅 **"Your site is live at ..."**，并给出链接
6. 这个链接就是部署地址，格式如：`https://iexplain.github.io/Tools/qiuzhilu/`
7. 用 iPhone Safari 打开这个完整链接 → 点分享 → **添加到主屏幕**，就搞定啦

## 如何添加新应用（重点）

1. 复制 `qiuzhilu/` 的完整文件夹，改名为你的新应用目录名
2. **必改 — 数据钥匙**：打开 `index.html`，搜索 `STORE_KEY`（约第 496 行），把
   `const STORE_KEY = 'interviewTracker.v1';` 改成唯一钥匙，如 `const STORE_KEY = 'notesApp.v1';`
   （同一个仓库多个应用必须用不同钥匙，否则数据会互相覆盖！）
3. **必改 — 缓存名**：打开 `sw.js`，把开头的 `CACHE` 和 `PREFIX` 两个常量改成新应用专属的名字：
   `const CACHE = 'notes-app-v1';` 和 `const PREFIX = 'notes-app-';`（`CACHE` 必须以 `PREFIX` 开头）。
   浏览器的缓存是**按域名共享**的，不按目录隔离，所以每个应用只清理自己前缀的旧缓存；
   如果几个应用用了同一个名字/前缀，就会互相把对方的缓存删掉，导致别的应用离线打不开。
   以后改了 `index.html` 想强制刷新缓存，只要把版本号往上加（`-v1` → `-v2`）即可。
4. **改应用名**：`index.html` 顶部的 `<title>` 和 `<meta name="apple-mobile-web-app-title">`、
   `manifest.json` 里的 `name` / `short_name`
5. **换图标（可选）**：改 `make_icons.py` 里的配色/图形后运行（需 Python + Pillow），
   或在线上传同名的 4 张图标即可
6. **加进入口页**：在根目录 `index.html` 的 `.app-list` 里照着已有的 `<a class="app-card">` 复制一份，
   改成新应用的链接、名字和描述
7. 新应用地址：`https://<你的用户名>.github.io/<仓库名>/<新应用目录>/`

## 注意事项

- 文件必须使用**相对路径**（`./index.html`、`icons/...`、`./manifest.json`），这样才能放在子目录下正常部署 —— 现有文件已全部是相对路径，直接复制即可。
- 每个应用目录内必须包含**完整一套**文件（index.html + manifest.json + sw.js + icons/），不能共用。
- `make_icons.py` 是图标生成工具脚本，可根据自己喜欢DIY。
- 有网时打开总是最新版；万一刷新后仍是旧版，关闭应用重新打开一次即可。
- 数据只在手机本地：删除主屏幕图标 / 清除浏览器网站数据会清空数据，建议定期在应用内「导出数据 → 备份全部数据（JSON）」保存备份。
- 导出的 CSV 里，以 `=` `+` `-` `@` 开头的备注会自动加一个前导单引号，防止 Excel 把它当公式执行；金额等纯数字不受影响。

