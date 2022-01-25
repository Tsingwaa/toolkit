import argparse
import io
import os

import cv2
import lmdb
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img-lst-path",
                        type=str,
                        help="input list including image name and category")
    parser.add_argument("--map-lst-path",
                        type=str,
                        help="input list including image category and label")
    parser.add_argument("--img-dir", type=str, help="input image dir")
    parser.add_argument("--lmdb-dir",
                        type=str,
                        help="directory to save .mdb and .lock file.")
    parser.add_argument("--resize",
                        action="store_true",
                        help="whether to resize")
    parser.add_argument("--height", type=int, default=224, help="input height")
    parser.add_argument("--width", type=int, default=224, help="input width")
    parser.add_argument("--use-cv2",
                        action="store_true",
                        default=True,
                        help="whether to use cv2 to resize")

    args = parser.parse_args()

    return args


def gen_lmdb(img_dir,
             img_lst_path,
             map_lst_path,
             lmdb_dir,
             resize=False,
             width=None,
             height=None,
             use_cv2=True):
    """Generate LMDB from image list
    Args:
        img_dir: directory to save images 
        img_lst_path(txt): (name category). Keep image name and corresponding category
        map_lst_path(txt): (category label). Keep all categories and corresponding label
        lmdb_dir: diretory to save the output lmdb files
        resize: resize scale. (width, height)
        use_cv2: if resize image, use cv2 or not.
    """

    print("======> Start generating LMDB...")

    if not os.path.isdir(lmdb_dir):
        os.mkdir(lmdb_dir)
    lmdb_env = lmdb.open(lmdb_dir, map_size=8589934592 * 50)
    lmdb_txn = lmdb_env.begin(write=True)

    map_ctg2label = {}
    with open(map_lst_path, 'r') as f:
        for line in f.readlines():
            ctg, label = line.strip().split('\t')
            map_ctg2label[ctg] = label
            # Write map (label:ctg) into lmdb
            lmdb_txn.put(str(label).encode(), ctg.encode())

    with open(img_lst_path, 'r') as f:
        num_samples = 0

        for idx, line in tqdm(enumerate(f.readlines())):
            img_name, img_ctg = line.strip().split('\t')
            img_path = os.path.join(img_dir, img_name)
            img_label = map_ctg2label[img_ctg]

            if not os.path.exists(img_path):  # filter
                continue

            if resize and (width is not None and height is not None):
                if use_cv2:
                    try:
                        img = cv2.imread(img_path)
                        img_resized = cv2.resize(img, (width, height))
                        img_ext = os.path.splitext(img_name)[-1]
                        img_buffer = cv2.imencode(img_ext, img_resized)[1]
                    except:
                        pass
            else:
                with open(img_path,
                          'rb') as f:  # 'rb' ensures that f.read() is 'Byte'
                    img_buffer = f.read()

            img_key = 'image-%09d' % (num_samples + 1)
            label_key = 'label-%09d' % (num_samples + 1)

            # Ensure that key and value are both 'Byte'
            lmdb_txn.put(img_key.encode(), img_buffer, overwrite=False)
            lmdb_txn.put(label_key.encode(),
                         str(label).encode(),
                         overwrite=False)

            num_samples += 1

        # Write sample numbers into lmdb
        lmdb_txn.put('num-samples'.encode(), str(num_samples).encode())
        lmdb_txn.commit()

    lmdb_env.sync()
    lmdb_env.close()
    print(f"=====> Done. \nLMDB save path: '{lmdb_dir}'")
    print(
        "===================================================================")


if __name__ == "__main__":

    args = parse_args()
    gen_lmdb(args.img_dir, args.img_lst_path, args.map_lst_path, args.lmdb_dir)
