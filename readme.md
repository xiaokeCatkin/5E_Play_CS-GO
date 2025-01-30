# 📊 CS:GO Match Data Analysis & Reporting Tool 🚀

## 项目概述 🎯

这款 Python 脚本工具箱，旨在帮助你从 [5EPlay](https://www.5eplay.com/) 平台轻松抓取、分析和报告你的 CS:GO 比赛数据。告别手动整理，让数据驱动你的游戏提升！ 📈

**核心功能一览:**

1. **数据抓取与导出 (`main_script.py`):**  🌊
   - 从 5EPlay API 自动化获取你的 CS:GO 比赛历史，包括比赛概况和详尽的玩家数据。
   - 内置**智能重试机制**，应对网络波动，确保数据抓取的稳定性。 💪
   - 将抓取的数据高效整理成结构化的 **Pandas DataFrames**。 🐼
   - 一键导出比赛汇总数据和玩家数据到 **Excel 文件 (`csgo_report.xlsx`)**，分 sheet 存储，清晰明了。 📁

2. **数据分析与玩家统计 (`analysis_script.py`):** 🔍
   - 轻松读取 `csgo_report.xlsx` 文件中的数据。
   - **个性化玩家筛选**：输入玩家昵称，快速聚焦特定玩家的比赛数据。 🧑‍🤝‍🧑
   - **灵活的数据筛选**：支持按时间范围和最近比赛场数筛选数据，满足不同分析需求。 ⏳
   - **组队局数据分析**：智能查找多位玩家共同参与的比赛，深度分析团队配合。 🤝
   - **详尽数据展示**：计算并展示玩家每场比赛数据和平均统计数据，洞察个人表现。 📊
   - **便捷数据导出**：将玩家的详细统计数据导出到独立的 **Excel 文件 (`player_detailed_stats.xlsx`)**，方便分享和存档。 📤

3. **Excel to JSON 转换 (`excel_to_json.py`):** 🔄
   - 快速读取 `csgo_report.xlsx` 文件中的 "比赛汇总" sheet。
   - 将比赛汇总数据无缝转换为 **JSON 格式 (`csgo_report.json`)**，方便与其他程序或应用集成使用。 🌐

## 技术原理详解 ⚙️

本项目巧妙地结合了以下技术和原理，打造高效的数据分析流程：

**1. 🚀 强大的 API 数据抓取 (Powered by `requests` 库):**

- **🌐 HTTP 请求:** 使用 `requests` 库向 5EPlay API 发送精准的 GET 请求，高效获取比赛数据。
- **🔑 API 端点 & 参数:**  通过深入分析 5EPlay 网页的开发者工具 (Network 面板)，精准定位 API 端点 (`https://gate.5eplay.com/crane/http/api/data`) 和必要的请求参数 (如 `match_type`, `page`, `uuid`, `start_time`, `end_time` 等)。
- **👤 模拟浏览器请求头 (Headers):**  巧妙地模拟浏览器行为，设置 `User-Agent` 和 `Referer` 请求头，并通过 `Authorization: Bearer {BEARER_TOKEN}` 头部进行身份验证。
- **🔄 智能重试机制 (Leveraging `urllib3.Retry` & `requests.adapters.HTTPAdapter`):**  为了应对不可预测的网络波动或服务器瞬时故障，精心配置请求重试策略。当 API 返回特定错误状态码 (500, 502, 503, 504) 时，程序将自动重试请求，显著提升程序的健壮性。
- **⚠️  SSL 证书验证 (开发阶段临时关闭 `verify=False`):**  在开发阶段为了简化流程，*临时* 关闭了 SSL 证书验证。 **🚨 重要提示：生产环境中，请务必启用 SSL 证书验证 (`verify=True`)，以确保数据传输的安全性！**
- **❗ 健壮的错误处理:**  运用 `try-except` 结构捕获 `requests.exceptions.RequestException` 异常，妥善处理 API 请求失败的情况，并输出清晰的错误信息，方便问题排查。

**2. 🐼 高效的数据处理与分析 (Driven by `pandas` 库):**

- **📊 数据结构化:**  将 API 返回的原始 JSON 数据巧妙地转化为 Pandas DataFrames，构建起结构化数据，为后续的数据操作和分析奠定坚实基础。
- **🧹 精细的数据清洗 & 转换:**
    - **⏱️ 时间戳转换:**  运用 `datetime.fromtimestamp` 函数，将原始时间戳数据转换为易于理解的日期时间格式。
    - **🗺️ 字段名称映射:**  借助 `FIELD_MAPPING` 字典，将 API 返回的专业英文技术字段名，映射为用户友好的中文名称，提升可读性。
    - **🔢 数据类型转换:**  根据数据特性，精确地将特定字段转换为合适的数值类型 (`float`, `int`)，为后续的数值计算铺平道路。
    - **🏆 胜负结果解读:**  智能解析 API 返回的布尔值 `is_win`，将其转换为直观的 "胜利" 或 "失败" 文字，结果一目了然。
    - **⏱️ 比赛时长计算:**  通过精妙的时间差计算，即 "结束时间" 减去 "开始时间"，精确获取比赛的持续时间，量化比赛时长。
- **🔎 灵活的数据筛选 & 过滤:**  `analysis_script.py` 脚本中，巧妙运用 Pandas 强大的条件筛选功能，根据用户指定的玩家昵称、时间范围、比赛场数等多元条件，精准过滤数据，聚焦分析目标。
- **📈 深入的数据聚合 & 统计:**  巧妙结合 `groupby` 和 `mean` 等 Pandas 核心函数，对数据进行分组聚合，计算玩家的关键平均统计数据，例如平均击杀数、平均死亡数等，量化玩家的整体表现。
- **🔗 无缝数据合并:**  巧妙运用 `pd.merge` 函数，以 "比赛ID" 为桥梁，将玩家数据与比赛汇总数据进行高效合并，补充比赛开始时间等关键信息，构建完整的数据视图。

**3. 📤 便捷的数据导出 (Powered by `pandas` 库):**

- **📊 Excel 导出:**  借助 `pd.ExcelWriter`，将精心处理的 DataFrames 数据，以 sheet 页的形式导出到 Excel 文件 (`.xlsx`) 中，方便用户在熟悉的 Excel 环境中进行查阅和深入分析。
- **📜 JSON 导出:**  运用 `df.to_json` 函数，将 DataFrame 数据导出为轻量级的 JSON 文件，`orient="records"` 参数确保 JSON 数据以记录列表的形式存储，`force_ascii=False` 和 `indent=4` 参数则保证生成的中文 JSON 文件具有良好的可读性。

**4. ⏰ 精确的时区处理 (`datetime` 库 & `timezone.utc`):**

- 为了消除潜在的时区警告，在时间戳转换环节，明确指定 `timezone.utc`，确保时间转换的精准性和一致性，避免因时区差异导致的数据偏差。

## 🛠️ 使用准备

在开始使用本项目之前，请确保你的环境满足以下条件：

1. **🐍 Python 版本:**  需要 **Python 3.6 或更高版本**。 建议使用最新稳定版 Python。
2. **📦 Python 依赖库:**  安装以下必要的 Python 库：
   - `requests`: 用于发送 HTTP 请求。 `pip install requests`
   - `pandas`: 用于数据处理和分析。 `pip install pandas`
   - `urllib3`:  `requests` 库的依赖，用于配置重试策略 (通常随 `requests` 安装)。 `pip install urllib3`
   - `openpyxl`: 用于写入 Excel 文件 (Pandas 安装时通常会自动安装)。 `pip install openpyxl`

3. **🔑 5EPlay API 密钥 (BEARER_TOKEN) & 用户 UUID:**
   - 你需要拥有一个 5EPlay 账号，并登录 [5EPlay 竞技平台](https://www.5eplay.com/)。
   - **🔑 获取 BEARER_TOKEN:** 登录 5EPlay 网页后，按 **F12** 打开浏览器开发者工具，切换到 **"Network" (网络)** 面板。随便刷新页面，找到任意一个 API 请求 (例如获取比赛列表的请求)。查看该请求的 **"Headers" (请求头)**，找到 `Authorization: Bearer {YOUR_TOKEN}`，复制 `Bearer` 后面的 **Token 值**。
   - **🆔 获取 UUID:**  在 5EPlay 个人主页的 **URL** 中，或者在 API 返回的 **用户信息** 中可以找到你的 UUID。
   - 将获取到的 `BEARER_TOKEN` 和 `UUID` 填入 `main_script.py` 脚本的 **配置参数** 部分。

## 🚀 快速上手指南

**1. ⚙️ 配置 `main_script.py`:**

   - 打开 `main_script.py` 文件。
   - 找到 **配置参数** 部分，填入你的 `BEARER_TOKEN` 和 `UUID`。
   - 可选：根据需要调整 `max_pages` (默认 3，限制抓取页数)、 `start_time` 和 `end_time` (时间戳格式，设置抓取比赛数据的时间范围)。

**2. 🏃 运行 `main_script.py` (数据抓取):**

   - 打开 **命令行** 或 **终端**，导航到脚本所在目录。
   - 执行命令： `python main_script.py`
   - 脚本开始从 5EPlay API 抓取数据，并将结果导出到 `csgo_report.xlsx` 文件。

**3. 📊 运行 `analysis_script.py` (数据分析):**

   - 确保已运行 `main_script.py` 并生成 `csgo_report.xlsx`。
   - 在 **命令行** 或 **终端** 中，导航到脚本目录。
   - 执行命令： `python analysis_script.py`
   - 按照提示，输入要对比的玩家昵称 (逗号分隔)、时间范围、比赛场数、是否组队局等信息。
   - 脚本将在终端展示分析结果，并询问是否导出详细数据到 `player_detailed_stats.xlsx`。

**4. 🔄 运行 `excel_to_json.py` (Excel 转 JSON):**

   - 确保已运行 `main_script.py` 并生成 `csgo_report.xlsx`。
   - 在 **命令行** 或 **终端** 中，导航到脚本目录。
   - 执行命令： `python excel_to_json.py`
   - 脚本会将 `csgo_report.xlsx` 的 "比赛汇总" sheet 转换为 `csgo_report.json` 文件。

## 📤 输出文件说明

- **`csgo_report.xlsx`:**  核心数据报告 Excel 文件。
    - **Sheet: 比赛汇总:**  包含所有抓取比赛的概览信息，例如：
        - `比赛ID`: 比赛的唯一标识符。
        - `地图`: 比赛地图名称。
        - `胜负`: 比赛结果（胜利/失败）。
        - `开始时间`, `结束时间`: 比赛开始和结束的时间戳（已转换为易读格式）。
        - ... 以及其他比赛基本信息。
    - **Sheet: 玩家数据:**  包含每场比赛中所有玩家的详细统计数据，例如：
        - `比赛ID`: 关联的比赛 ID。
        - `玩家_username`: 玩家昵称。
        - `玩家_kill`, `玩家_death`: 玩家的击杀数和死亡数。
        - `fight_RWS评分`, `fight_Rating`, `fight_ADR`: 玩家在比赛中的 RWS, Rating, ADR 等战斗数据。
        - ... 以及其他玩家详细比赛数据。

- **`player_detailed_stats.xlsx`:** (由 `analysis_script.py` 生成)  玩家详细统计 Excel 文件。
    - 针对每个分析的玩家，生成独立的 Sheet 页：
        - **Sheet: `{玩家昵称}_每场比赛数据`:**  列出该玩家筛选出的每场比赛的详细数据记录，方便逐场分析。
        - **Sheet: `{玩家昵称}_平均数据`:**  展示该玩家在筛选出的所有比赛中的各项关键数据的平均值，用于评估玩家的整体水平。

- **`csgo_report.json`:** (由 `excel_to_json.py` 生成)  比赛汇总 JSON 文件。
    - 包含 `csgo_report.xlsx` 文件中 "比赛汇总" sheet 的 JSON 格式数据，方便程序化读取和使用。

## ✨ 未来展望

- **⚙️ 配置文件化:**  将 API 密钥、UUID、时间范围、页数等配置项移至独立的配置文件 (如 `.ini` 或 `.json`)，提升配置管理的便捷性。
- **📈 更丰富的数据分析功能:**  在 `analysis_script.py` 中拓展更多高级数据分析功能，例如：
    -  计算更全面的玩家指标：胜率、KD 比率、爆头率、KAST 等。
    -  多维度数据分析：按地图、比赛模式、武器等维度进行数据分组和深度分析。
    -  可视化报表生成：集成图表库 (如 `matplotlib`, `seaborn`, `plotly`)，生成直观的统计图表，辅助数据解读。
- **🖥️ 图形用户界面 (GUI):**  为数据分析脚本开发友好的图形用户界面 (例如使用 `Tkinter`, `PyQt`, `wxPython` 等)，降低使用门槛，提升用户体验。
- **💾 数据持久化:**  引入数据库 (如 SQLite, MySQL, PostgreSQL) 对抓取的数据进行持久化存储，实现数据的长期管理和高效检索，避免重复抓取。
- **⏰ 自动化数据抓取:**  集成定时任务工具 (如 `cron` 或 Windows 任务计划程序)，实现定期自动运行 `main_script.py`，抓取最新的比赛数据，保持数据更新。
- **📝 完善的日志记录:**  使用 `logging` 模块记录程序运行日志，包括错误、警告、信息等，方便问题追踪和程序维护。
- **✅ 强化数据验证与清洗:**  在数据处理流程中，增加数据验证和清洗环节，处理异常值、缺失值等，提高数据质量和分析结果的可靠性。

## ⚠️ 重要声明

本项目仅为 **学习交流和个人使用** 而设计。请务必遵守 5EPlay 平台的服务条款和 API 使用协议。 **请勿滥用 API 接口，避免对平台服务器造成不必要的压力。**

**🔒 API 密钥 (BEARER_TOKEN) 属于敏感信息，请务必妥善保管，切勿泄露！**

**本项目不对因使用此工具可能产生的任何问题承担责任。**  请使用者自行承担所有风险。