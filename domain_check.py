import dns.resolver
import json

def check_domains(*domains, dns_server="1.1.1.1", target_value="cdn.tysgos.com."):
    host_headers = ['', 'www', 'm']
    results = []

    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = [dns_server]  # 使用者指定的 DNS 伺服器

    for domain in domains:
        for host in host_headers:
            #刪除根域的前段(.)
            full_domain = f"{host}.{domain}".lstrip('.')
            try:
                records= dns.resolver.query(full_domain, 'CNAME')
                for record in records:
                    if record.to_text() == target_value:
                        results.append((full_domain, "✔️", record.to_text()))
                    else:
                        results.append((full_domain, "❌", record.to_text()))
            except dns.resolver.NoAnswer:
                results.append((full_domain, "❌", "沒找到 CNAME 記錄"))
            except dns.resolver.NXDOMAIN:
                results.append((full_domain, "❌", "不存在"))
            except Exception as e:
                results.append((full_domain, "❌", f"發生未知錯誤: {e}"))
    # 將結果分成正確和錯誤兩個清單
    correct_results = [result for result in results if result[1] == "✔️"]
    incorrect_results = [result for result in results if result[1] == "❌"]
    # 先輸出錯誤結果
    for result in incorrect_results:
        print(f"{result[1]} 域名: {result[0]}，解析值: {result[2]}")
    # 再輸出正確結果
    for result in correct_results:
        print(f"{result[1]} 域名: {result[0]}，解析值: {result[2]}")

def read_file(path):
    with open(str(path), 'r') as file:
        lines  = file.readlines()
        domain_list = ','.join([f'{line.strip()}' for line in lines])
    return domain_list

if __name__ == '__main__' :

    target=f't.txt'
    domain_list = read_file(target)
    domains = domain_list.split(',')

    check_domains(*domains)
