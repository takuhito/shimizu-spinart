import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The broken block looks like this (with potential line breaks and mess):
# <mt:Var name="video_url" regex_replace="/^.*(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?"\'<>]*).*/" ,"https://www.youtube.com/embed/$1" setvar="embed_url" />

# We want to replace it with a clean, escaped version.
# We will match the whole mt:Var tag that sets embed_url.

# Regex to find the broken tag. It likely spans multiple lines now or has broken attributes.
# We look for <mt:Var name="video_url" ... setvar="embed_url" />
# We use a broad match to capture the mess.
pattern = r'<mt:Var name="video_url"\s+regex_replace=[\s\S]*?setvar="embed_url"\s*/>'

# The correct tag with escaped characters in regex_replace
# We use &quot; for ", &#39; for ', &lt; for <, &gt; for >
# regex_replace="/...([^#\&\?&quot;&#39;&lt;&gt;]*).../"
correct_tag = '<mt:Var name="video_url" regex_replace="/^.*(?:youtu\\.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=|\\&v=|shorts\\/)([^#\\&\\?&quot;&#39;&lt;&gt;]*).*/" ,"https://www.youtube.com/embed/$1" setvar="embed_url" />'

def replacement_func(match):
    return correct_tag

new_content = re.sub(pattern, replacement_func, content)

# Also fix the like="<iframe" to be safe, although " might be the only real issue.
# But < inside attribute can be risky in some parsers.
# Let's keep like="<iframe" for now as it's likely valid if quoted, but if it fails we can try &lt;iframe.
# Given the error was "ContentField mismatch", it was likely due to the tag being malformed and eating the closing tags or confusing the parser structure.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed syntax errors.")
