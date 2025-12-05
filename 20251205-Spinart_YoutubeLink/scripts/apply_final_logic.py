import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The final robust logic block.
# 1. Use MATCH detection for iframes.
# 2. Use single quotes for regex_replace attribute, double quotes for replacement string.
# 3. Use hex codes for special chars in regex.
# 4. NO </mt:Else> tag.

final_logic = """<mt:Var name="video_raw" regex_replace='/<iframe/i","MATCH"' setvar="iframe_check" />
                                            <mt:If name="iframe_check" like="MATCH">
                                                <mt:Var name="video_raw" />
                                            <mt:Else>
                                                <mt:Var name="video_raw" regex_replace="/\s+/" ,"" setvar="video_url" />
                                                <mt:Var name="video_url" regex_replace='/.*?(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?\\x22\\x27\\x3c\\x3e]*).*/',"https://www.youtube.com/embed/$1" ' setvar="embed_url" />
                                                <iframe width="560" height="315" src="<mt:Var name='embed_url' />" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                                            </mt:Else>
                                            </mt:If>"""

# Function to apply logic to a block
def apply_logic(content, col_num, suffix_type):
    # suffix_type is "Long" or "" (empty for short)
    field_name = f"コラム{col_num}-ビデオ{suffix_type}"
    
    # Pattern matches the div content for the specific field
    # We look for the simplified version or the previous safe version.
    # To be safe, we match everything inside the div.
    pattern = f'(<mt:ContentField content_field="{field_name}">[\s\S]*?<div class="embed-responsive embed-responsive-16by9">)([\s\S]*?)(</div>)'
    
    def replacement_func(match):
        prefix = match.group(1)
        suffix = match.group(3)
        return f'{prefix}\n                                            {final_logic}\n                                        {suffix}'

    return re.sub(pattern, replacement_func, content, count=1)

# Iterate over columns 01 to 05
for i in range(1, 6):
    col_num = f"{i:02d}" # 01, 02, 03, 04, 05
    content = apply_logic(content, col_num, "Long")
    content = apply_logic(content, col_num, "")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied final robust video logic to Columns 01-05.")
