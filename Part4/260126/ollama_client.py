# import requests
# import time
#
# url ="http://localhost:11434/api/generate"
#
# payload = {
# "model":"llama3.2:3b",
# "prompt":"FastAPI가 뭔지 한 문장으로.",
# "stream":True
# }
#
# times = []
# for i in range(5):
#     start = time.time()
#     res = requests.post(url, json=payload)
#     elapsed = time.time() - start
#     times.append(elapsed)
# print(f"[{i+1}/5] latency={elapsed:.2f}s")
#
# print("\nAVG latency:",sum(times)/len(times))


import requests
import time

url ="http://localhost:11434/api/generate"

payload = {
"model":"llama3.2:3b",
"prompt":"AI모델에서 양자화가 뭔지 3줄로 설명해줘.",
"stream":False,
}

start = time.time()
res = requests.post(url, json=payload)
elapsed = time.time() - start

data = res.json()
print("=== Model Response ===")
print(data["response"])
print("\n=== Latency ===")
print(f"{elapsed:.2f}s")