import re

file_path = '/Users/takuhito/Library/CloudStorage/Dropbox-Design/藤田拓人/★★★Antigravity-Dev/MofuttoGEN/記事テンプレート.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

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
                                        </script>"""

# Pattern to match <$mt:cvideoXX(long)?$>
# We want to capture the whole tag to wrap it in SetVarBlock
# Regex: <\$mt:cvideo\d+(?:long)?\$>
pattern = r'(<\$mt:cvideo\d+(?:long)?\$>)'

def replacement_func(match):
    original_tag = match.group(1)
    # Wrap in SetVarBlock and append JS logic
    return f'<mt:SetVarBlock name="video_raw">{original_tag}</mt:SetVarBlock>{js_logic}'

new_content = re.sub(pattern, replacement_func, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Applied JavaScript-based video logic to Article Template.")
