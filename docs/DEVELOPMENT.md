# 开发指南

## 前置要求

- Linux / Windows
- Git
- uv

## 本地环境

```zsh
git clone https://github.com/ilearnings/cs-autoexec.git
cd cs-autoexec
uv sync --project keymap
```

`uv sync` 只在首次或依赖变更后执行

## 本地生成

```zsh
uv run --project keymap python keymap/main.py
```

一条命令完成: 解析 `autoexec.cfg` -> 生成中间文件 -> 渲染 SVG -> 写入时间戳

产物:

- `keymap/keymap.yml`: 标签映射
- `images/bindings.svg`: 绑定图

可重复执行, 每次覆盖旧时间戳

## 本地预览

浏览器打开 `images/bindings.svg`

## 修改内容

只处理 `autoexec.cfg` 中 `bind` 开头的行, 用 `^...^` 标记按键标签:

```cfg
bind "a" "+forward" // ^左移^
```

无 `^...^` 的键显示键名 (灰色)

## 渲染与排版规则

`keymap` 模块对文字深度定制, 规则如下:

### 1. 标签换行规则

按优先级拆分, 命中即生效:

| 顺序 | 规则 | 示例 | 结果 |
| :--- | :--- | :--- | :--- |
| 1 | 已含 `\n` | `A\nB` | 原样 |
| 2 | 含 `/` | `AK47 / M4系列` | 两行 |
| 3 | 含中文 `-` | `滚轮-跳` | 两行 |
| 4 | 前缀 (`BOT` / `R Shift` 等) | `BOT原地添加` | 两行 |
| 5 | 纯中文 (含数字) | `中性名切换` | 两行 |
| 6 | 长度 > 6 | `ABCDEFG` | 两行 |
| 7 | 以上都不命中 | `AK47` | 原样 |

> 注: 纯中文拆分时, 3 字及以下不拆, 偶数均分, 奇数上排最多 3 字. 超过 **8 字** 时打印警告 (本地/Actions), 建议缩短.

### 2. 鼠标特殊渲染规则

- **滚轮合并**: 当 `MWHEELUP` 与 `MWHEELDOWN` 描述完全一致时, 自动隐藏下滚, 并在滚轮中心竖向排版显示 (如"滚\n轮\n跳"); 若不一致则上下分开显示.
- **中键 (飞行/标记)**: 居中显示在滚轮正下方.
- **侧键上 (雷达切换)**: 靠左对齐, 贴合侧键弧度.
- **侧键下 (全装备)**: 强制**竖向单字排列** (如"全\n装\n备"), 靠左对齐, 完美嵌入细长侧键.

```cfg
// 滚轮合并触发示例
bind "MWHEELUP" "+jump" // ^滚轮跳^
bind "MWHEELDOWN" "+jump" // ^滚轮跳^
```

## 提交并推送

```zsh
git add .
git commit -m "update bindings"
git push
```

push 后 Actions 自动运行并提交产物

## 触发条件

仅当 push 到 `main` 且改动含 `autoexec.cfg` 时触发. 改其他文件不触发, 如需手动跑一次, 在 GitHub 网页编辑 `autoexec.cfg` 的任意 `^...^` 标签并 commit

## 文件结构

```text
cs-autoexec/
├── .github/
│   ├── dependabot.yml                    ✅ Dependabot 更新配置
│   └── workflows/
│       ├── automerge.yml                 ✅ Dependabot PR 自动合并
│       └── update.yml                    ✅ 键位图生成工作流
├── autoexec.cfg                          ✅ 源配置
├── docs/
│   └── DEVELOPMENT.md                    ✅ 开发文档
├── images/
│   ├── bindings.svg                      🔄 绑定图(自动生成)
│   └── mouse.png                         ✅ 鼠标配置截图
├── keymap/
│   ├── canvas.py                         ✅ 画布缩放与时间戳注入
│   ├── config.yml                        ✅ keymap-drawer 渲染配置
│   ├── constants.py                      ✅ 全部常量、正则与鼠标 SVG
│   ├── keymap.yml                        🔄 中间产物(自动生成)
│   ├── label.py                          ✅ 文字换行、对齐与渲染逻辑
│   ├── layout.json                       ✅ 键盘物理布局
│   ├── main.py                           ✅ 主流程控制与文件解析
│   ├── pyproject.toml                    ✅ 依赖声明
│   └── uv.lock                           🔄 依赖锁定(自动生成)
└── README.md                             ✅ 说明文档
```
