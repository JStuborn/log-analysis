import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

emails      = []
passwords   = []
domains     = []

data_dir = './data'
email_pass_regex = re.compile(r'([^:]+):([^:]+)')

for file_name in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file_name)
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            match = email_pass_regex.match(line.strip())
            if match:
                email, password = match.groups()
                emails.append(email)
                passwords.append(password)
                domain = email.split('@')[-1]
                domains.append(domain)

df = pd.DataFrame({'email': emails, 'password': passwords, 'domain': domains})

top_passwords = df['password'].value_counts().head(10)
top_domains = df['domain'].value_counts().head(10)
top_emails = df['email'].value_counts().head(10)
password_length = df['password'].apply(len)

def analyze_complexity(pwd):
    return {
        'has_upper': any(c.isupper() for c in pwd),
        'has_lower': any(c.islower() for c in pwd),
        'has_digit': any(c.isdigit() for c in pwd),
        'has_special': any(c in "!@#$%^&*()-_=+" for c in pwd)
    }

complexity = df['password'].apply(analyze_complexity).apply(pd.Series)
complexity_summary = complexity.sum()

plt.figure(figsize=(10,6))
sns.barplot(x=top_passwords.values, y=top_passwords.index, palette='viridis')
plt.title('Top 10 Most Common Passwords')
plt.xlabel('Frequency')
plt.ylabel('Passwords')
plt.show()

plt.figure(figsize=(10,6))
top_domains.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette('Set3'), shadow=True)
plt.title('Top 10 Email Domains')
plt.ylabel('')
plt.show()

plt.figure(figsize=(10,6))
sns.histplot(password_length, bins=20, kde=True, color='blue')
plt.title('Password Length Distribution')
plt.xlabel('Password Length')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(10,6))
complexity_summary.plot(kind='bar', color='orange')
plt.title('Password Complexity Distribution')
plt.xlabel('Criteria')
plt.ylabel('Count')
plt.show()
