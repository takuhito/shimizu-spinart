import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Canonical content for a video block
# We will insert this inside <mt:ContentField ...> ... </mt:ContentField>
canonical_body = """
                                    <mt:ContentFieldValue setvar="video_raw" />
                                    <div class="col-md-6">
                                        <div class="embed-responsive embed-responsive-16by9">
                                            <mt:Var name="video_raw" />
                                        </div>
                                    </div>"""

# Function to deep clean a block
def deep_clean(content, col_num, suffix_type):
    # suffix_type is "Long" or "" (empty for short)
    field_name = f"コラム{col_num}-ビデオ{suffix_type}"
    
    # Pattern matches the entire ContentField block
    # (<mt:ContentField content_field="FIELD_NAME">)([\s\S]*?)(</mt:ContentField>)
    pattern = f'(<mt:ContentField content_field="{field_name}">)([\s\S]*?)(</mt:ContentField>)'
    
    def replacement_func(match):
        prefix = match.group(1)
        suffix = match.group(3)
        # We replace the middle part with canonical body
        return f'{prefix}{canonical_body}\n                                {suffix}'

    return re.sub(pattern, replacement_func, content, count=1)

# Iterate over columns 01 to 05
for i in range(1, 6):
    col_num = f"{i:02d}" # 01, 02, 03, 04, 05
    content = deep_clean(content, col_num, "Long")
    content = deep_clean(content, col_num, "")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Deep cleaned all video blocks for Columns 01-05.")
