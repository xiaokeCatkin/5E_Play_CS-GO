import pandas as pd  # 导入 pandas

# 读取Excel文件
try:
    df = pd.read_excel("csgo_report.xlsx", sheet_name="比赛汇总")
except FileNotFoundError:
    print("错误：找不到文件 'csgo_report.xlsx'。请确保文件存在于脚本所在的目录中。")
    exit() # 退出程序，避免后续错误

# 转换为JSON并保存
try:
    df.to_json("csgo_report.json", orient="records", force_ascii=False, indent=4) # 添加 indent 参数以格式化 JSON 输出
    print("JSON 文件 'csgo_report.json' 已成功生成。")
except Exception as e:
    print(f"转换到 JSON 时发生错误：{e}")