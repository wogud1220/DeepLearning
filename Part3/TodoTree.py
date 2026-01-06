# TODO
# FIXME
# WARNING
# CHECKLIST
# BUG


from dotenv import load_dotenv

# API KEY 정보로드
load_dotenv()

import os

print(f"[API KEY]\n{os.environ['OPENAI_API_KEY']}")
