def clean_data(src_path, tgt_path):
    """Remove the overlap img urls and PIL-unreadable-data urls.
    Source file(txt): url category
    Target file(txt): img_fname category
    """
    import os
    from tqdm import tqdm
    import collections
     
    img_fname2ctg = dict()
    overlap_set = set()
    with open(src_path, 'r') as f_src, open(tgt_path, 'w') as f_tgt:
        for line in tqdm(f_src.readlines(), desc='Checking overlap urls...'):
            url, category = line.strip().split('\t')
            img_fname = os.path.split(url)[-1]
            
            # check PIL-unreadable data extension
            if not check_extension(img_fname, {'.mp4', '.mov', '.m4v', '.gif'}): 
                if img_fname[-4] != '.' and img_fname[-5] != '.':
                    img_fname += '.jpg'

                if img_fname not in img_fname2ctg.keys(): 
                    img_fname2ctg[img_fname] = category
                else:  # Once the url occurs before, add it into overlap_set
                    overlap_set.add(img_fname)
        
        valid_img_cnt = 0
        valid_ctg_set = set()
        for img_fname, category in tqdm(img_fname2ctg.items(), desc='Writing clean data...'):
            if img_fname not in overlap_set:  # Only collect those urls excluded overlap_set
                valid_img_cnt += 1
                valid_ctg_set.add(category)
                line = f'{img_fname}\t{category}\n'
                f_tgt.write(line) 
    
    print(f'Total valid images: {valid_img_cnt}\t Total valid categories: {len(valid_ctg_set)}')
    print(f'Total overlap urls: {len(overlap_set)}')

def check_extension(fname, ext_set=None):
    """Check if given url has readable extension.
    Args: 
        fname(str):
        ext_set(set): 

    Return(bool)
    """
    if ext_set is None:
        ext_set = {'.jpg', '.JPG', '.jpeg', '.JPEG', '.png', '.PNG', 
                '.bmp', '.BMP', '.webp', '.WEBP', '.jfif', '.JFIF'}

    if fname[-4:] in ext_set or fname[-5:] in ext_set:
        return True
    else:
        return False


if __name__ == '__main__':
    src_path = '/home/hadoop-mtcv/cephfs/data/zengchenghua/projects/data/youxuan_anno/grocery_label_data.txt'
    tgt_path = '/home/hadoop-mtcv/cephfs/data/zengchenghua/projects/data/youxuan_anno/grocery_label_data_ex_overlap.txt'
    clean_data(src_path, tgt_path)

