import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match the block inside <div class="embed-responsive ..."> ... </div> for コラム01-ビデオ
# It is preceded by <mt:ContentField content_field="コラム01-ビデオ"> ... <div class="embed-responsive embed-responsive-16by9">

pattern = r'(<mt:ContentField content_field="コラム01-ビデオ">[\s\S]*?<div class="embed-responsive embed-responsive-16by9">)([\s\S]*?)(</div>)'

def replacement_func(match):
    prefix = match.group(1)
    suffix = match.group(3)
    return f'{prefix}\n                                                    <mt:Var name="video_raw" />\n                                                {suffix}'

new_content = re.sub(pattern, replacement_func, content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Simplified Column 01 Video (Short) block.")
