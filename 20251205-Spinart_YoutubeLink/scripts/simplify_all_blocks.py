import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Function to simplify a block
def simplify_block(content, col_num, suffix_type):
    # suffix_type is "Long" or "" (empty for short)
    field_name = f"コラム{col_num}-ビデオ{suffix_type}"
    
    # Pattern matches the div content for the specific field
    # <mt:ContentField content_field="FIELD_NAME"> ... <div class="embed-responsive ..."> ... </div>
    pattern = f'(<mt:ContentField content_field="{field_name}">[\s\S]*?<div class="embed-responsive embed-responsive-16by9">)([\s\S]*?)(</div>)'
    
    def replacement_func(match):
        prefix = match.group(1)
        suffix = match.group(3)
        return f'{prefix}\n                                            <mt:Var name="video_raw" />\n                                        {suffix}'

    return re.sub(pattern, replacement_func, content, count=1)

# Iterate over columns 01 to 05
for i in range(1, 6):
    col_num = f"{i:02d}" # 02, 03, 04, 05
    content = simplify_block(content, col_num, "Long")
    content = simplify_block(content, col_num, "")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Simplified video blocks for Columns 02-05.")
