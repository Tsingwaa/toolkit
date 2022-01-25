import numpy as np
import torch
import torch.nn as nn
import torchvision

model = torchvision.models.resnet50()
model.cuda()
model = nn.DataParallel(model)

img = torch.from_numpy(np.random.random(500, 3, 224, 224)) \
        .astype(np.float32).cuda()

while True:
    model(img)
    # time.sleep(0.1)
