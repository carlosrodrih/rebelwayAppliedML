import sys
import importlib
from PIL import Image
import hou

#Scripts path
sys.path.append(r"D:\development\rebelwayML\WEEK3\scripts")

#Load and reload modules
import cd_utils
importlib.reload(cd_utils)
from cd_utils import CdUtils
import nn_utils
importlib.reload(nn_utils)
from nn_utils import NNUtils

node_path = "/obj/grid1/classifyfashionmnist/OUT_GEO"
font_path = "/obj/grid1/classifyfashionmnist/font1"
img_path = "D:/development/rebelwayML/WEEK3/scripts/output/output.png"

def run():
    CdUtils.test()
    matrix = CdUtils.cd_to_matrix(node_path)
    if hou.pwd().parm("save").eval():
        img = CdUtils.matrix_to_image(matrix,img_path)
    else:
        img = CdUtils.matrix_to_image(matrix)  
    model_path = hou.pwd().parm("model").eval()
    prediction = NNUtils.predict(model_path, img)
    text = f"Prediction: {prediction}"
    font_node = hou.node(font_path)
    font_node.parm('text').set(text)
