import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/新ファイル.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The JS-based logic block.
# We output the raw content in a hidden div.
# We add a target div for the video.
# We add a script to process it.
# Note: We'll add the script ONCE at the end of the file or inline for each block?
# Inline is safer for scope, but repetitive.
# Let's use a common class and a single script at the bottom?
# Or just inline script for immediate execution (simpler for now).

# Actually, to avoid script tag repetition, I'll use a specific structure and one script at the end of the body?
# But I don't want to parse the whole file to find the end of body.
# I'll put the script inline but check if it's already defined? No, just use an IIFE.

js_logic = """
                                            <div class="js-video-raw" style="display:none;"><mt:Var name="video_raw" /></div>
                                            <div class="js-video-target"></div>
                                            <script>
                                            (function() {
                                                var currentScript = document.currentScript;
                                                var container = currentScript.parentElement; // The .embed-responsive div
                                                var rawDiv = container.querySelector('.js-video-raw');
                                                var targetDiv = container.querySelector('.js-video-target');
                                                var rawContent = rawDiv.innerHTML.trim();

                                                // Decode HTML entities if needed (MT might encode them)
                                                var txt = document.createElement("textarea");
                                                txt.innerHTML = rawContent;
                                                var decodedContent = txt.value;

                                                if (decodedContent.indexOf('<iframe') !== -1) {
                                                    // It's an iframe
                                                    targetDiv.innerHTML = decodedContent;
                                                } else {
                                                    // It's a URL
                                                    // Extract ID
                                                    var url = decodedContent.trim();
                                                    // Remove whitespace
                                                    url = url.replace(/\\s+/g, '');
                                                    
                                                    var videoId = '';
                                                    var match = url.match(/(?:youtu\\.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=|\\&v=|shorts\\/)([^#\\&\\?\\"\\'<>]*)/);
                                                    if (match && match[1]) {
                                                        videoId = match[1];
                                                        var embedUrl = 'https://www.youtube.com/embed/' + videoId;
                                                        targetDiv.innerHTML = '<iframe width="560" height="315" src="' + embedUrl + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>';
                                                    } else {
                                                        // Fallback: just show text or link?
                                                        // For now, leave empty or show text
                                                        // targetDiv.textContent = url; 
                                                    }
                                                }
                                            })();
                                            </script>
"""

# Function to apply logic to a block
def apply_logic(content, col_num, suffix_type):
    # suffix_type is "Long" or "" (empty for short)
    field_name = f"コラム{col_num}-ビデオ{suffix_type}"
    
    # Pattern matches the div content for the specific field
    pattern = f'(<mt:ContentField content_field="{field_name}">[\s\S]*?<div class="embed-responsive embed-responsive-16by9">)([\s\S]*?)(</div>)'
    
    def replacement_func(match):
        prefix = match.group(1)
        suffix = match.group(3)
        return f'{prefix}\n                                            {js_logic}\n                                        {suffix}'

    return re.sub(pattern, replacement_func, content, count=1)

# Iterate over columns 01 to 05
for i in range(1, 6):
    col_num = f"{i:02d}" # 01, 02, 03, 04, 05
    content = apply_logic(content, col_num, "Long")
    content = apply_logic(content, col_num, "")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied JavaScript-based video logic to Columns 01-05.")
