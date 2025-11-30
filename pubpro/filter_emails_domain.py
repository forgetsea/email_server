import pandas as pd

# === 1. 读取Excel文件 ===
a_df = pd.read_excel("temp/A_list.xlsx")
b_df = pd.read_excel("temp/emails.xlsx")

# === 2. 提取A列表中所有邮箱后缀 ===
def extract_domain(email):
    if isinstance(email, str) and '@' in email:
        return email.split('@')[1].strip().lower()
    return None

a_domains = set(a_df['Email'].dropna().apply(extract_domain))

# === 3. 过滤B列表 ===
def is_domain_allowed(email):
    if isinstance(email, str) and '@' in email:
        domain = email.split('@')[1].strip().lower()
        return domain not in a_domains
    return False

filtered_b = b_df[b_df['Email'].apply(is_domain_allowed)]

# === 4. 导出结果 ===
filtered_b.to_excel("B_filtered.xlsx", index=False)
print(f" filted {len(b_df)} emails，left {len(filtered_b)} emails")
