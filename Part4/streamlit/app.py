
spam_words = "광고, 모델, , ㅁㄴㅇㄹ "
keywords = [k.strip() for k in spam_words.split(",") if k.strip()]

"광고", "모델", "", "ㅁㄴㅇㄹ "
"광고, 모델, , ㅁㄴㅇㄹ "

print(keywords)