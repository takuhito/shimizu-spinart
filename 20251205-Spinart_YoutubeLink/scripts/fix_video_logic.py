import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the robust block
# 1. Detect iframe using regex_replace (replaces <iframe with MATCH)
# 2. Check if result contains MATCH
# 3. If Else, extract ID using Hex codes for quotes/brackets to avoid syntax errors and character class bugs.
#    Regex: /.*?(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?\x22\x27\x3c\x3e]*).*/
#    We use non-greedy start .*? to find the first occurrence.

robust_block = """<mt:Var name="video_raw" regex_replace="/<iframe/i","MATCH" setvar="iframe_check" />
                                            <mt:If name="iframe_check" like="MATCH">
                                                <mt:Var name="video_raw" />
                                            <mt:Else>
                                                <mt:Var name="video_raw" regex_replace="/\\s+/" ,"" setvar="video_url" />
                                                <mt:Var name="video_url" regex_replace="/.*?(?:youtu\\.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=|\\&v=|shorts\\/)([^#\\&\\?\\x22\\x27\\x3c\\x3e]*).*/" ,"https://www.youtube.com/embed/$1" setvar="embed_url" />
                                                <iframe width="560" height="315" src="<mt:Var name='embed_url' />" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                                            </mt:Else>
                                            </mt:If>"""

# We need to replace the existing blocks.
# The existing blocks are messy due to previous edits.
# They start with <mt:If name="video_raw" like=... (or similar) and end with </mt:If> inside the embed-responsive div.
# But wait, I previously replaced them with a block starting with <mt:If name="video_raw" like="<iframe">
# and ending with </mt:If>.
# I should match that structure.

# Pattern to match the current block in the file.
# It starts with <mt:If name="video_raw" like= and ends with </mt:If>
# It might have <mt:Else> inside.
pattern = r'<mt:If name="video_raw" like=[\s\S]*?</mt:If>'

# Use a replacement function
def replacement_func(match):
    return robust_block

new_content = re.sub(pattern, replacement_func, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Applied robust video logic.")
