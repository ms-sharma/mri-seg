import os
from torch.utils.data import Dataset
from PIL import Image
from torchvision.transforms import Compose
from utils.transforms import OneHotEncode


# The Images are first cropped as PIL Images
crop_size = (0,0,200,200)

def get_pairs(filename):
    f = open(filename,'r')
    names = [name.strip() for name in f.readlines()]
    pairs = []

    for i in range(len(names)):
        pairs.append((names[i],names[i]))

    return pairs
"""
    This returns slice pairs from same images
"""
class IBSRv2(Dataset):
    TRAIN_LIST = 'lists/train_list.txt'
    VAL_LIST = 'lists/val_list.txt'

    def __init__(self,root,datadir,mode="train",
                co_transform=Compose([]),img_transform=Compose([]),
                label_transform=Compose([])):
        self.root = root
        self.datadir = datadir
        self.mode = mode
        self.co_transform = co_transform
        self.img_transform = img_transform
        self.label_transform = label_transform

        self.pairlist = get_pairs(os.path.join(self.root,"datasets",self.TRAIN_LIST)) if self.mode == "train" else get_pairs(os.path.join(self.root,"datasets",self.TRAIN_LIST))

    def __getitem__(self,index):
        fname1,fname2 = self.pairlist[index]

        with open(os.path.join(self.datadir,"img",fname1+".tif"),'rb') as f:
            img1 = Image.open(f).crop(crop_size)
        with open(os.path.join(self.datadir,"img",fname2+".tif"),'rb') as f:
            img2 = Image.open(f).crop(crop_size)
        with open(os.path.join(self.datadir,"cls",fname1+".png"),'rb') as f:
            label1 = Image.open(f).convert('P').crop(crop_size)
        with open(os.path.join(self.datadir,"cls",fname2+".png"),'rb') as f:
            label2 = Image.open(f).convert('P').crop(crop_size)
        # import pdb; pdb.set_trace()
        img1,label1 = self.co_transform((img1,label1))
        img2,label2 = self.co_transform((img2,label2))
        img1 = self.img_transform(img1)
        img2 = self.img_transform(img2)
        label1 = self.label_transform(label1)
        label2 = self.label_transform(label2)

        ohlabel1 = OneHotEncode()(label1)
        return ((img1,label1,fname1),(img2,label2,fname2),ohlabel1)

    def __len__(self):
        return len(self.pairlist)
