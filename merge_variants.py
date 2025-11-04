#!/usr/bin/env python3
import pandas as pd
import sys
import os
import re

def process_variants(input_file, output_file, merge_option):
    """
    合并变体的函数
    """
    print(f"Processing file: {input_file}")
    print(f"Output file: {output_file}")
    print(f"Merge option: {merge_option}")
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} does not exist!")
        return
    
    # 读取输入文件，先尝试检测分隔符
    try:
        # 读取前几行来检测分隔符
        with open(input_file, 'r') as f:
            first_line = f.readline().strip()
            second_line = f.readline().strip()
        
        print(f"First line: {repr(first_line)}")
        print(f"Second line: {repr(second_line)}")
        
        # 检测分隔符：如果包含tab，用tab；否则用空格分隔
        if '\t' in second_line:
            separator = '\t'
            print("Using TAB separator")
        else:
            separator = r'\s+'  # 使用正则表达式匹配多个空格
            print("Using space separator")
        
        # 读取数据
        df = pd.read_csv(input_file, sep=separator, engine='python')
        print(f"Input file shape: {df.shape}")
        print(f"Column names: {list(df.columns)}")
        print(f"Data types before conversion:")
        print(df.dtypes)
        
        # 确保 count 和 CPM 列是数值类型
        df['count'] = pd.to_numeric(df['count'], errors='coerce')
        df['CPM'] = pd.to_numeric(df['CPM'], errors='coerce')
        
        print(f"Data types after conversion:")
        print(df.dtypes)
        
        # 检查是否有 NaN 值
        print(f"NaN values in count: {df['count'].isna().sum()}")
        print(f"NaN values in CPM: {df['CPM'].isna().sum()}")
        
        print(f"First few rows after type conversion:")
        print(df.head())
        
        # 检查重复的 sncRNAs
        duplicates = df['sncRNAs'].duplicated().sum()
        print(f"Number of duplicate sncRNAs before processing: {duplicates}")
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    if merge_option.lower() == "yes":
        print("Merging variants...")
        # 创建新的第一列，去掉|后面的部分
        df['sncRNAs_clean'] = df['sncRNAs'].str.split('|').str[0]
        
        print(f"Sample of cleaned sncRNAs:")
        print(df[['sncRNAs', 'sncRNAs_clean']].head())
        
        # 检查清理后的重复情况
        duplicates_clean = df['sncRNAs_clean'].duplicated().sum()
        print(f"Number of duplicate cleaned sncRNAs: {duplicates_clean}")
        
        # 按照清理后的第一列和第五列（sample）分组，合并第三列（count）和第四列（CPM）
        # 修正：添加所有需要保留的列
        merged_df = df.groupby(['sncRNAs_clean', 'sample']).agg({
            'length': 'max',
            'count': 'sum',
            'CPM': 'sum'
        }).reset_index()
        
        # 重命名列
        merged_df = merged_df.rename(columns={'sncRNAs_clean': 'sncRNAs'})
        
        # 重新排列列的顺序
        merged_df = merged_df[['sncRNAs', 'length', 'count', 'CPM', 'sample']]
        print(f"After merging shape: {merged_df.shape}")
        print("Sample of merged data:")
        print(merged_df.head())
        
        # 再次检查是否还有重复的 sncRNAs
        final_duplicates = merged_df['sncRNAs'].duplicated().sum()
        print(f"Number of duplicate sncRNAs after merging: {final_duplicates}")
        
        if final_duplicates > 0:
            print("Warning: Still have duplicates after merging!")
            print("Duplicate examples:")
            duplicated_mask = merged_df['sncRNAs'].duplicated(keep=False)
            print(merged_df[duplicated_mask].head(10))
            
            # 如果仍有重复，进一步合并
            print("Performing additional merge by sncRNAs and sample...")
            merged_df = merged_df.groupby(['sncRNAs', 'sample']).agg({
                'length': 'first',  # 取第一个长度值
                'count': 'sum',
                'CPM': 'sum'
            }).reset_index()
            
            merged_df = merged_df[['sncRNAs', 'length', 'count', 'CPM', 'sample']]
            final_duplicates = merged_df['sncRNAs'].duplicated().sum()
            print(f"After additional merge - duplicate sncRNAs: {final_duplicates}")
        
    else:
        print("Not merging variants...")
        # 如果不合并，检查原始数据的重复情况
        duplicates = df['sncRNAs'].duplicated().sum()
        if duplicates > 0:
            print(f"Warning: Original data has {duplicates} duplicate sncRNAs!")
            print("You may need to merge variants to resolve duplicates.")
        merged_df = df
    
    # 保存结果，使用TAB分隔符
    try:
        merged_df.to_csv(output_file, sep='\t', index=False)
        print(f"Successfully wrote {merged_df.shape[0]} rows to {output_file}")
        
        # 最终检查
        final_duplicates = merged_df['sncRNAs'].duplicated().sum()
        if final_duplicates == 0:
            print("✓ No duplicate sncRNAs in output file")
        else:
            print(f"⚠ Warning: {final_duplicates} duplicate sncRNAs still exist in output file")
            
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_variants.py <input_file> <output_file> <merge_variants(yes/no)>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    merge_option = sys.argv[3]
    
    process_variants(input_file, output_file, merge_option)
