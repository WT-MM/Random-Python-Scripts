from retrieve import Retrieve
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--images', help="Root directory containing images", type=str)
parser.add_argument('--directory','-d', help="Directory to store image file", default=os.getcwd(), type=str)
parser.add_argument('--name', help="Name of image file", default="1", type=str)
parser.add_argument("--output", help="File output type", default="png", choices=["png", "jpg"], type=str)
parser.add_argument('--uniform', help="Uniformity of image dimensions", default=False, type=bool)
parser.add_argument('--division', help="Number of columns used", default=4, type=int)

args = vars(parser.parse_args())


imgRetrieval = Retrieve(args['images'])
imgs = imgRetrieval.findImgs()

if(args['uniform']):

else:
    sds

