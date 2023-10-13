# %%
import argparse
import xml.etree.ElementTree as ET
from PIL import Image
import os

def parse():
    parser = argparse.ArgumentParser(description='Crop IAM dataset')
    parser.add_argument("--annotation_folder", type=str, default="./", help="A positional integer argument")
    parser.add_argument("--image_folder", type=str, default="./", help="A positional integer argument")
    parser.add_argument("--annotation_out_folder", type=str, default="./", help="A positional integer argument")
    parser.add_argument("--image_out_folder", type=str, default="./", help="A positional integer argument")
    parser.add_argument("--max", type=int, default=10, help="A positional integer argument")

    args = parser.parse_args()
    return args

# %% [markdown]
# ## Loading Image and Annotation
def main():

    args = parse()
    annotation_folder = args.annotation_folder
    image_folder = args.image_folder
    annotation_out_folder = args.annotation_out_folder
    image_out_folder = args.image_out_folder
    amt = args.max

    # %%
    files = os.listdir(annotation_folder)
    for file in files[:amt]:
        try:
            file = file.split(".")[0]

            # %%
            tree = ET.parse(os.path.join(annotation_folder,f"{file}.xml"))
            root = tree.getroot()

            # %%
            image =  Image.open(os.path.join(image_folder,f"{file}.png"))

            # %% [markdown]
            # ## Crop Images

            # %%
            left, right = 0, image.size[0]

            # %%
            items = root.findall('.//line')
            upper = min([int(item.attrib['asy']) for item in items])
            lower = max([int(item.attrib['dsy'])+abs(int(item.attrib['dss']))/1000/180*4*right for item in items])

            # %%
            cropped_image = image.crop((left, upper-20, right, lower+50))

            # %%
            os.makedirs(image_out_folder,exist_ok=True)

            # %% [markdown]
            # ## Loading Label

            # %%
            items = root.findall('.//machine-print-line')
            reference = " ".join([item.attrib['text'] for item in items])

            # %%
            os.makedirs(annotation_out_folder,exist_ok=True)

        except Exception as e:
            print(e)
        else:
            cropped_image.save(os.path.join(image_out_folder,f"{file}.png"))
            with open(os.path.join(annotation_out_folder,f"{file}.txt"),'w') as f:
                f.write(reference)            


if __name__ == "__main__":
    main()


