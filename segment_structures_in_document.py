"""
 * This Software is under the MIT License
 * Refer to LICENSE or https://opensource.org/licenses/MIT for more information
 * Written by ©Kohulan Rajan 2020
"""
import sys
import os
from decimer_segmentation import segment_chemical_structures_from_file
from decimer_segmentation import save_images, get_bnw_image, get_square_image
import numpy as np

def main():
    """
    This script segments chemical structures in a document, saves the original
    segmented images as well as a binarized image and a an undistorted square
    image
    """
    if len(sys.argv) != 2:
        print("Usage of this function: convert.py input_path")
    if len(sys.argv) == 2:
        # Extract chemical structure depictions and save them
        raw_segments_list, bboxes_list, shape_list = segment_chemical_structures_from_file(sys.argv[1])
        segment_dir = os.path.join(f"{sys.argv[1]}_output", "segments")

        # let file name give page number tag
        id_count=0
        fig_count=0
        coordinate_list=[]
        pdf_shape_list=[]
        for raw_segments,bboxes,shape in zip(raw_segments_list,bboxes_list,shape_list):
            if shape[2]!=0:
                save_images(
                    raw_segments, segment_dir, f"{os.path.split(sys.argv[1])[1][:-4]}_{str(id_count)}_orig"
                )
                coordinate_list.append(np.array(bboxes))
                # pdf_shape_list.append(shape)
                fig_count+=shape[2]
            pdf_shape_list.append(shape)
            id_count+=1
        # ======= this is other 2 formats 
        # # Get binarized segment images
        # binarized_segments = [get_bnw_image(segment) for segment in raw_segments_list]
        # save_images(
        #     binarized_segments, segment_dir, f"{os.path.split(sys.argv[1])[1][:-4]}_bnw"
        # )
        # # Get segments in size 299*299 and save them
        # normalized_segments = [
        #     get_square_image(segment, 299) for segment in raw_segments_list
        # ]
        # save_images(
        #     normalized_segments,
        #     segment_dir,
        #     f"{os.path.split(sys.argv[1])[1][:-4]}_norm",
        # )

        print(f"Segments saved at {segment_dir}.")

        # output coordinate list
        coordinate_dir=os.path.join(f"{sys.argv[1]}_output")

        # coordinate_final [number of figs,4]
        coordinate_final=np.zeros((fig_count,4))
        start_id=0
        for i in np.arange(0,len(coordinate_list)):
            coordinate_final[start_id:start_id+coordinate_list[i].shape[0],:]=coordinate_list[i]
            start_id+=coordinate_list[i].shape[0]
        # for coord_every_page in coordinate_list:
        #     coordinate_final[]

        np.savetxt(coordinate_dir+"/fig_coords.txt",coordinate_final,fmt="%d")
        pdf_shape=np.array(pdf_shape_list)
        np.savetxt(coordinate_dir+"/pdf-shape.txt",pdf_shape,fmt="%d")
        


if __name__ == "__main__":
    main()
