import gzip  # 引入gzip模块
from Bio import SeqIO
import hashlib

# 读取 tDR.fa 并计算每个序列的 MD5 值
tDR_file = snakemake.config.get("tDR_file", "sRNA-indexes/tDR/tDR_55.fa")
tDR_seq_name_map = {}  # 存储 MD5 映射关系
tDR_name_count_map = {}
tDR_name_length_map = {}
output_name_order = []  # 存储输出数据顺序

# 初始化map的值
with open(tDR_file, "r") as handle:
    for record in SeqIO.parse(handle, "fasta"):
        tDR_sequence = str(record.seq)
        tDR_seq_name_map[tDR_sequence] = record.id  # 使用序列的MD5哈希值作为键
        tDR_name_length_map[record.id] = len(tDR_sequence)
        tDR_name_count_map[record.id] = 0
        output_name_order.append(record.id)  # 正确地使用append方法

# 处理 FASTQ 文件，更新计数
fastq_file = snakemake.input.fastq_file
unmapped_file = snakemake.output.unmapped_file

with open(fastq_file, "r") as fq_handle, gzip.open(unmapped_file, "wt") as um_handle:
    for record in SeqIO.parse(fq_handle, "fastq"):
        fq_read_seq = str(record.seq)
        if fq_read_seq in tDR_seq_name_map:  # 检查read值是否在映射的键中
            tDR_name = tDR_seq_name_map[fq_read_seq]
            tDR_name_count_map[tDR_name] += 1  # 累加对应的计数
        else:
            # 如果没有匹配，输出到 unmapped.fastq.gz
            SeqIO.write(record, um_handle, "fastq")

# 创建初始输出文件
output_file = snakemake.output.output_file
with open(output_file, "w") as out_handle:
    out_handle.write("ReadName\tLength\tCount\n")
    for entry in output_name_order:
        out_handle.write(entry + '\t' + str(tDR_name_length_map[entry]) + '\t' + str(tDR_name_count_map[entry]) + '\n')

print("Processing complete.")
