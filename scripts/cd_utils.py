import hou
import math
import numpy as np
from PIL import Image

class CdUtils:

    @staticmethod
    def cd_to_matrix(node_path: str):
        print("Converting Cd to Matrix...")
        node = hou.node(node_path)
        geo = node.geometry()
        prims = geo.prims()
        num_prims = len(prims)
        num_rows = num_columns = int(math.sqrt(num_prims))

        grid_matrix = []
        for row in range(num_rows):
            new_row = []
            for col in range(num_columns):
                prim_index = row * num_columns + col
                if prim_index < num_prims:
                    prim = prims[prim_index]
                    # Leer componente R del atributo Cd, o 0 si no existe
                    cd = prim.attribValue("Cd")[0] if prim.attribValue("Cd") else 0.0
                    new_row.append(cd)
                else:
                    new_row.append(0.0)
            grid_matrix.append(new_row)
        print("Done!")
        return grid_matrix

    @staticmethod
    def matrix_to_image(matrix, output_path=None):
        print("Converting matrix to image...")
        np_matrix = np.array(matrix) * 255
        np_matrix = np_matrix.astype(np.uint8)

        img = Image.fromarray(np_matrix, mode='L')

        if output_path:
            img.save(output_path)
            print(f"Image saved in {output_path}...")

        print("Image ready.")
        return img

    @staticmethod
    def test():
        print("")
