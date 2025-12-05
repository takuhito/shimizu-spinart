import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def count_tags(tag_name):
    # Case insensitive search for opening and closing tags
    # Opening: <mt:TagName ...> or <mt:TagName>
    # Closing: </mt:TagName>
    
    # Note: mt:ContentField can be self-closing <mt:ContentField ... />? No, usually not for blocks.
    # But let's check for / at the end of opening tag just in case.
    
    open_pattern = re.compile(f'<mt:{tag_name}\\b[^>]*>', re.IGNORECASE)
    close_pattern = re.compile(f'</mt:{tag_name}>', re.IGNORECASE)
    
    open_tags = open_pattern.findall(content)
    close_tags = close_pattern.findall(content)
    
    # Filter out self-closing tags from open_tags if any (e.g. <mt:ContentField ... />)
    real_open_tags = [t for t in open_tags if not t.strip().endswith('/>')]
    
    print(f"Tag: {tag_name}")
    print(f"  Opening: {len(real_open_tags)}")
    print(f"  Closing: {len(close_tags)}")
    
    if len(real_open_tags) != len(close_tags):
        print(f"  MISMATCH! Diff: {len(real_open_tags) - len(close_tags)}")

count_tags('ContentField')
count_tags('If')
count_tags('Else') # Else is usually self-closing or just a separator, so mismatch is expected if we count </mt:Else> which shouldn't exist.
