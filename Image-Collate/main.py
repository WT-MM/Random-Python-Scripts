from retrieve import Retrieve
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--images', help="Root directory containing images", type=str)
parser.add_argument('--directory','-d', help="Directory to store image file", default=os.getcwd(), type=str)
parser.add_argument('--name', help="Name of image file", default="1", type=str)

args = vars(parser.parse_args())


imgRetrieval = Retrieve(args['images'])