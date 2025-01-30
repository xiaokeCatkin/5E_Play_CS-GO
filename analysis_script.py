import pandas as pd
import numpy as np

def load_and_filter_data(excel_file, player_names):
    """加载数据并筛选指定玩家的数据，并合并比赛开始时间"""
    try:
        player_df = pd.read_excel(excel_file, sheet_name="玩家数据")
        if player_df.empty:
            print("警告: '玩家数据' sheet 为空。")
            return None
        
        filtered_data = player_df[player_df['玩家_username'].isin(player_names)]
        if filtered_data.empty:
             print(f"警告: 没有找到匹配 {' '.join(player_names)} 的数据。")
             return None
        
        #加载比赛汇总表
        match_df = pd.read_excel(excel_file, sheet_name="比赛汇总")
        if match_df.empty:
            print("警告: '比赛汇总' sheet 为空，无法获取比赛开始时间。")
            return filtered_data

        # 确保 '比赛ID' 列的数据类型匹配
        filtered_data['比赛ID'] = filtered_data['比赛ID'].astype(str)
        match_df['比赛ID'] = match_df['比赛ID'].astype(str)
        
        # 合并数据, 使用左连接保证所有玩家数据都保留
        merged_data = pd.merge(filtered_data, match_df[['比赛ID', '开始时间']], on='比赛ID', how='left')
        
        if '开始时间' not in merged_data.columns:
            print("警告: '比赛汇总' 表中没有 '开始时间' 列，无法按时间排序。")
            return filtered_data

        return merged_data

    except FileNotFoundError:
        print(f"错误: 文件 '{excel_file}' 未找到。")
        return None
    except Exception as e:
         print(f"读取 Excel 文件时发生错误: {str(e)}")
         return None

def find_common_matches(filtered_data, player_names):
      """查找所有玩家共同参与的比赛ID"""
      if filtered_data is None:
          return None
      
      match_ids = [filtered_data[filtered_data['玩家_username'] == name]['比赛ID'].unique() for name in player_names]
      
      if not match_ids:
            return None

      common_match_ids = set(match_ids[0])
      for ids in match_ids[1:]:
          common_match_ids.intersection_update(ids)

      if not common_match_ids:
          print("警告：没有找到这些玩家共同参与的比赛。")
          return None
      return list(common_match_ids)
    
def filter_by_match_count(filtered_data, player_names, match_count, common_match_ids, start_date=None, end_date=None):
    """筛选指定场数或时间范围内的比赛数据"""
    if filtered_data is None:
      return None
    if common_match_ids is not None:
         filtered_data = filtered_data[filtered_data['比赛ID'].isin(common_match_ids)]
         
    filtered_match_data = pd.DataFrame()
    for player_name in player_names:
        player_data = filtered_data[filtered_data['玩家_username'] == player_name].copy()
        if player_data.empty:
            print(f"警告: 找不到玩家 {player_name} 的数据")
            continue
           
        # 检查 '开始时间' 是否存在
        if '开始时间' not in player_data.columns:
            print(f"警告: 玩家 {player_name} 的数据中缺少 '开始时间' 列，无法按时间排序。")
            filtered_match_data = pd.concat([filtered_match_data, player_data], ignore_index=True)
            continue
        
        player_data['开始时间'] = pd.to_datetime(player_data['开始时间'], errors='coerce')
       
        #时间范围筛选
        if start_date and end_date:
            player_data = player_data[(player_data['开始时间']>=start_date) & (player_data['开始时间']<=end_date)]
        
        if player_data.empty:
           print(f"警告： 玩家 {player_name} 在指定时间范围内没有数据。")
           continue

        if match_count != float('inf'):
             player_data = player_data.sort_values(by='开始时间', ascending=False)
             if len(player_data) < match_count:
               print(f"警告: 玩家 {player_name} 在指定时间范围内的比赛场数少于 {match_count} 场.")
               match_count_for_player = len(player_data)
             else:
               match_count_for_player = match_count
            
             selected_data = player_data.head(match_count_for_player)
        else:
             selected_data = player_data

        filtered_match_data = pd.concat([filtered_match_data, selected_data], ignore_index=True)
        
    return filtered_match_data


def process_player_data(filtered_data, player_names):
    """处理玩家数据，提取每场比赛数据和平均数据"""
    if filtered_data is None:
        return None
    
    all_player_data = {}
    for player_name in player_names:
      player_df = filtered_data[filtered_data['玩家_username']==player_name]
      if player_df.empty:
        print(f"警告：找不到玩家 {player_name} 的数据")
        continue
      
      player_match_data = {}
      match_ids = player_df['比赛ID'].unique()
      for match_id in match_ids:
            match_df = player_df[player_df['比赛ID'] == match_id]
            match_data = match_df.to_dict(orient='records')
            player_match_data[match_id] = match_data
            
      numeric_columns = [col for col in player_df.columns if player_df[col].dtype in [np.int64, np.float64]]
      average_data = player_df[numeric_columns].mean().to_dict()
      all_player_data[player_name] = {'match_data':player_match_data, 'average_data':average_data}
      
    return all_player_data

def display_player_data(all_player_data):
    """展示玩家每场比赛数据和平均数据"""
    if not all_player_data:
        print("没有可显示的数据。")
        return
    
    for player_name, data in all_player_data.items():
        print(f"\n--- {player_name} 的数据 ---")
        print("每场比赛数据:")
        for match_id, match_data in data['match_data'].items():
             print(f"    比赛ID: {match_id}")
             match_df = pd.DataFrame(match_data)
             print(match_df)
        print("\n平均数据:")
        avg_df = pd.DataFrame(data['average_data'], index=[0])
        print(avg_df)


def export_player_data_to_excel(all_player_data, filename="player_detailed_stats.xlsx"):
    """将玩家详细数据导出到 Excel 文件"""
    if not all_player_data:
        print("没有可导出的数据。")
        return

    with pd.ExcelWriter(filename) as writer:
         for player_name, data in all_player_data.items():
             #每场比赛数据
             match_data_list = []
             for match_id, match_data in data['match_data'].items():
                 match_df = pd.DataFrame(match_data)
                 match_data_list.append(match_df)
             if match_data_list:
                match_data_all = pd.concat(match_data_list, ignore_index= True)
                match_data_all.to_excel(writer, sheet_name=f"{player_name}_每场比赛数据", index=False)
                
             #平均数据
             avg_df = pd.DataFrame(data['average_data'], index=[0])
             avg_df.to_excel(writer, sheet_name=f"{player_name}_平均数据", index=False)

    print(f"\n详细数据已导出到 {filename}")


# ======================
# 主程序逻辑
# ======================
def main():
    excel_file = "csgo_report.xlsx"  # 替换你的文件名
    player_names_input = input("请输入要对比的玩家昵称，用逗号分隔: ")
    player_names = [name.strip() for name in player_names_input.split(",")]
    
    filtered_data = load_and_filter_data(excel_file, player_names)
    if filtered_data is None:
        return
    
    if filtered_data is not None:
       print(filtered_data.columns)

    time_range_input = input("是否按时间范围筛选数据？(y/n): ").lower()
    start_date, end_date = None, None
    if time_range_input == "y":
        try:
            start_date_str = input("请输入开始日期 (YYYY-MM-DD): ")
            end_date_str = input("请输入结束日期 (YYYY-MM-DD): ")
            start_date = pd.to_datetime(start_date_str)
            end_date = pd.to_datetime(end_date_str)
        except (ValueError, TypeError):
            print("日期格式不正确，将不使用时间范围筛选。")
            start_date, end_date = None, None


    match_count_input = input("请输入要对比的最近场数，默认为全部 (输入数字): ")
    try:
       match_count = int(match_count_input) if match_count_input else float('inf')
    except ValueError:
        print("输入的场数无效，使用全部场数")
        match_count = float('inf')
        
    team_match_input = input("是否只对比组队局的数据？ (y/n): ").lower()
    common_match_ids = None
    if team_match_input == "y":
         common_match_ids = find_common_matches(filtered_data, player_names)
         if common_match_ids is None:
            return
      
    filtered_data = filter_by_match_count(filtered_data, player_names, match_count, common_match_ids, start_date, end_date)
    if filtered_data is None:
        return
    
    player_data = process_player_data(filtered_data, player_names)
    if player_data:
        display_player_data(player_data)
        export_excel = input("是否将详细数据导出到excel(y/n)？")
        if export_excel.lower() == "y":
            export_player_data_to_excel(player_data)

if __name__ == "__main__":
    main()