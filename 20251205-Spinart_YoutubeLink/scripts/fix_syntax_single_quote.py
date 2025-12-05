import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace the &quot; mess with clean single-quoted attributes.

# Target 1:
# regex_replace="&quot;/<iframe/i&quot;,&quot;MATCH&quot;"
# Replacement:
# regex_replace='/<iframe/i","MATCH"'

# Target 2:
# regex_replace="&quot;/.*?(?:...)([^#\&\?\x22\x27\x3c\x3e]*).*/&quot; ,&quot;https://www.youtube.com/embed/$1&quot;"
# Replacement:
# regex_replace='/.*?(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?\x22\x27\x3c\x3e]*).*/","https://www.youtube.com/embed/$1"'

# Note: The regex in Target 2 is long.
# Let's match the whole mt:Var tag and replace it with a clean version.

# Clean Block Logic
# <mt:Var name="video_raw" regex_replace='/<iframe/i","MATCH"' setvar="iframe_check" />
# <mt:If name="iframe_check" like="MATCH">
#     <mt:Var name="video_raw" />
# <mt:Else>
#     <mt:Var name="video_raw" regex_replace="/\s+/" ,"" setvar="video_url" />
#     <mt:Var name="video_url" regex_replace='/.*?(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?\x22\x27\x3c\x3e]*).*/","https://www.youtube.com/embed/$1"' setvar="embed_url" />
#     <iframe width="560" height="315" src="<mt:Var name='embed_url' />" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
# </mt:Else>
# </mt:If>

clean_block = """<mt:Var name="video_raw" regex_replace='/<iframe/i","MATCH"' setvar="iframe_check" />
                                            <mt:If name="iframe_check" like="MATCH">
                                                <mt:Var name="video_raw" />
                                            <mt:Else>
                                                <mt:Var name="video_raw" regex_replace="/\\s+/" ,"" setvar="video_url" />
                                                <mt:Var name="video_url" regex_replace='/.*?(?:youtu\\.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=|\\&v=|shorts\\/)([^#\\&\\?\\x22\\x27\\x3c\\x3e]*).*/","https://www.youtube.com/embed/$1"' setvar="embed_url" />
                                                <iframe width="560" height="315" src="<mt:Var name='embed_url' />" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
                                            </mt:Else>
                                            </mt:If>"""

# Find the existing block. It starts with <mt:Var name="video_raw" regex_replace=... and ends with </mt:If>
# The start tag is messy now.
# Let's match from <mt:Var name="video_raw" regex_replace=... setvar="iframe_check" /> ... </mt:If>

pattern = r'<mt:Var name="video_raw"\s+regex_replace=[\s\S]*?</mt:If>'

def replacement_func(match):
    return clean_block

new_content = re.sub(pattern, replacement_func, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed syntax with single quotes.")
