import torch

a = torch.arange(12).reshape(3,4)
b = a.transpose(0,1)      # view
c = b.contiguous()        # 새 메모리

a[0,0] = 999
print("a:\n", a)
print("b:\n", b)          # 같이 바뀜
print("c:\n", c)          # 안 바뀜 (복사본)

torch.permute(a, (0, 2, 1))
print('그냥 서명swjaehyeongff')