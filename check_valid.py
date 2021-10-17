import os
import multiprocessing
from PIL import Image
from tqdm import tqdm

def test_readability(line):
    img_dir = '/ssd/data/chenghua_grocery/images/'
    img_name, category = line.strip().split('\t')
    img_path = os.path.join(img_dir, img_name)
    try:
        # Test cv2 read original image and read bytes stream
        cv2_img = cv2.imread(img_path)
        img_ext = os.path.splitext(img_name)[1]
        cv2_buf = cv2.imencode(img_ext, cv2_img) 
        cv2_img = cv2.imdecode(np.frombuffer(cv2_buf, np.uint8), 3)
        cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        # Test PIL.Image.open original image and bytes stream
        Image.open(img_path)
        # TODO
        pil_buf = six.BytesIO()
        buf.seek(0)
        Image.open(pil_buf).convert('RGB')
    except:
        print(f'{fname} is PIL-unreadable')
        image.close()
    else:
        image.close()
        return line        

def txt2list():
    src_fpath = '/home/hadoop-mtcv/cephfs/data/zengchenghua/projects/data/youxuan_anno/grocery_label_data_ex_overlap.txt'
    with open(src_fpath, 'r') as f:
        return f.readlines()

def callback_write(line):
    tgt_fpath = '/home/hadoop-mtcv/cephfs/data/zengchenghua/projects/data/youxuan_anno/grocery_label_data_ex_overlap_readable.txt'
    with open(tgt_fpath, 'a+') as f_tgt:
        f_tgt.write(line)
        print(f'W')


if __name__ == '__main__':
    src_fpath = '/home/hadoop-mtcv/cephfs/data/zengchenghua/projects/data/youxuan_anno/grocery_label_data_ex_overlap.txt'
    tgt_fpath = '/home/hadoop-mtcv/cephfs/data/zengchenghua/projects/data/youxuan_anno/grocery_label_data_ex_overlap_readable.txt'

    with open(src_fpath, 'r') as f:
        lines = f.readlines()

    pool = multiprocessing.Pool(24)
    for line in lines:
        pool.apply_async(func=test_readability, args=(line,), callback=callback_write)
    pool.close()
    pool.join()


