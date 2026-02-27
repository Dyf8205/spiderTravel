import os

log_file = os.path.join(os.path.dirname(__file__), "make_final_trip.log")
output_file = os.path.join(os.path.dirname(__file__), "error.log")

count = 0
with open(log_file, "r", encoding="utf-8") as f_in, \
     open(output_file, "w", encoding="utf-8") as f_out:
    for line in f_in:
        if "| ERROR" in line:
            f_out.write(line)
            count += 1

print(f"共过滤出 {count} 条 ERROR 日志，已写入 {output_file}")
