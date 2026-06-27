# See Desktop/rag-data/crawl_ks_v2.py for the complete script
# Key improvements over v1:
# - html_to_markdown() preserves image positions
# - make_image_src_map() maps original src -> local filenames
# - Auto-cleans WeChat template text
# - Better HTML->Markdown conversion (headings, bold, lists)

import os, sys, json, re, time, base64, hashlib
from datetime import datetime

# The full script is at C:/Users/jjdeng/Desktop/rag-data/crawl_ks_v2.py
# Due to size, only the new functions are documented here.
# See references/markdown-conversion-v2.md for the detailed implementation.
