import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace <mt:ContentFieldValue setvar="video_raw" /> 
# with <mt:SetVarBlock name="video_raw"><mt:ContentFieldValue /></mt:SetVarBlock>

# Pattern: <mt:ContentFieldValue setvar="video_raw" />
pattern = r'<mt:ContentFieldValue setvar="video_raw"\s*/>'
replacement = '<mt:SetVarBlock name="video_raw"><mt:ContentFieldValue /></mt:SetVarBlock>'

new_content = re.sub(pattern, replacement, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed variable capture logic in all occurrences.")
