import nmap

# 创建 Nmap 扫描器实例
nm = nmap.PortScanner()

# 执行 SYN 扫描（-sS）
nm.scan('192.168.1.1', '22-80', arguments='-sS')

# 输出扫描结果
print(nm.all_hosts())

