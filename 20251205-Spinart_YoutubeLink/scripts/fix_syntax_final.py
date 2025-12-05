import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to fix two things:
# 1. <mt:Var name="video_raw" regex_replace="/<iframe/i","MATCH" setvar="iframe_check" />
#    Should be: <mt:Var name="video_raw" regex_replace="&quot;/<iframe/i&quot;,&quot;MATCH&quot;" setvar="iframe_check" />
#    OR use single quotes for the attribute: regex_replace='/<iframe/i","MATCH'
#    Let's use single quotes for the attribute wrapper, it's cleaner if MT supports it.
#    Actually, standard HTML/XML parsers support single quotes. MTML should too.
#    But to be absolutely safe and consistent with previous fixes, let's use &quot; inside double quotes.

# 2. <mt:Var name="video_url" regex_replace="/.*?(?:...)([^#\&\?\x22\x27\x3c\x3e]*).*/" ,"https://www.youtube.com/embed/$1" setvar="embed_url" />
#    This definitely needs fixing.

# Let's define the correct blocks.

# Fix 1: iframe check
# Pattern: <mt:Var name="video_raw" regex_replace="/<iframe/i","MATCH" setvar="iframe_check" />
# We match loosely to catch variations.
pattern1 = r'<mt:Var name="video_raw" regex_replace="/<iframe/i","MATCH" setvar="iframe_check"\s*/>'
replacement1 = '<mt:Var name="video_raw" regex_replace="&quot;/<iframe/i&quot;,&quot;MATCH&quot;" setvar="iframe_check" />'

# Fix 2: URL extraction
# Pattern: <mt:Var name="video_url" regex_replace="/.*?([^"]*).*/" ,"https://www.youtube.com/embed/$1" setvar="embed_url" />
# This is hard to match with regex because of the complex regex inside.
# Let's match by the setvar="embed_url" and the start of the tag.
pattern2 = r'<mt:Var name="video_url" regex_replace="/.*?\(\?:youtu\.be\\/\|v\\/\|u\\/\\w\\/\|embed\\/\|watch\\\?v=\|\\&v=\|shorts\\/\)\(\[\^#\\&\\\?\\x22\\x27\\x3c\\x3e\]\*\)\.\*/" ,"https://www.youtube.com/embed/\$1" setvar="embed_url"\s*/>'
# The above pattern is getting very complicated and error prone to write.
# Let's try a simpler approach: match the line content if possible.
# Or match: <mt:Var name="video_url" regex_replace=... setvar="embed_url" />
pattern2_simple = r'<mt:Var name="video_url" regex_replace="[\s\S]*?" ,"https://www.youtube.com/embed/\$1" setvar="embed_url"\s*/>'

# Actually, let's just use the known bad string and replace it.
bad_string1 = '<mt:Var name="video_raw" regex_replace="/<iframe/i","MATCH" setvar="iframe_check" />'
good_string1 = '<mt:Var name="video_raw" regex_replace="&quot;/<iframe/i&quot;,&quot;MATCH&quot;" setvar="iframe_check" />'

bad_string2_part = 'regex_replace="/.*?(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?\x22\x27\x3c\x3e]*).*/" ,"https://www.youtube.com/embed/$1"'
# We need to escape the quotes in the bad string for the replacement logic? No, just string replacement.
# But the bad string in the file has unescaped quotes.

# Let's construct the good string 2.
# regex_replace="&quot;/.*?(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?\x22\x27\x3c\x3e]*).*/&quot; ,&quot;https://www.youtube.com/embed/$1&quot;"
good_string2_part = 'regex_replace="&quot;/.*?(?:youtu\\.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=|\\&v=|shorts\\/)([^#\\&\\?\\x22\\x27\\x3c\\x3e]*).*/&quot; ,&quot;https://www.youtube.com/embed/$1&quot;"'

# Perform replacements
new_content = content.replace(bad_string1, good_string1)

# For the second one, since it's long and complex, let's use regex to find the tag and replace the attribute part.
# Find: regex_replace="...pattern..." ,"replacement"
# Replace with: regex_replace="&quot;...pattern...&quot; ,&quot;replacement&quot;"

def replace_quotes_in_match(match):
    full_match = match.group(0)
    # The match is the whole tag.
    # We want to replace the regex_replace attribute value's quotes.
    # But wait, the attribute value itself is broken.
    # It looks like: regex_replace="/pattern/" ,"replacement"
    # We want: regex_replace="&quot;/pattern/&quot; ,&quot;replacement&quot;"
    
    # Let's just hardcode the replacement for the specific line we know we wrote.
    # We wrote: <mt:Var name="video_url" regex_replace="/.*?(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?\x22\x27\x3c\x3e]*).*/" ,"https://www.youtube.com/embed/$1" setvar="embed_url" />
    
    # We can just replace the specific substring of the attribute.
    target = 'regex_replace="/.*?(?:youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|shorts\/)([^#\&\?\x22\x27\x3c\x3e]*).*/" ,"https://www.youtube.com/embed/$1"'
    replacement = 'regex_replace="&quot;/.*?(?:youtu\\.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=|\\&v=|shorts\\/)([^#\\&\\?\\x22\\x27\\x3c\\x3e]*).*/&quot; ,&quot;https://www.youtube.com/embed/$1&quot;"'
    
    return full_match.replace(target, replacement)

# Regex to find the tag
pattern_tag = r'<mt:Var name="video_url" regex_replace=[\s\S]*?setvar="embed_url"\s*/>'
new_content = re.sub(pattern_tag, replace_quotes_in_match, new_content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed syntax errors final.")
