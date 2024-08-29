
import os
import boto3
from PIL import Image
import numpy as np


# Initializing the S3 client on "requirements.txt" file. 
s3 = boto3.client('s3') # CUrrently not using S3. 

def encode_image(image_path):
    try:
        #Opening the sample image file.
        with Image.open(image_path) as img:
            # Resizing the images to a fixed size
            img = img.resize((224, 224))

            # Converting the image to a numpy array
            img_array = np.array(img)

            # Flatten the array and normalize the values 
            vector = img_array.flatten() / 255.0 

            # #Normilizing the vector 
            # vector = vector / 255.0

        return vector  # Converting numpy array to list for Json serialization
    except Exception as e:
        print(f"Error processing image {image_path}: {str(e)}")
        return None



def lambda_handler(event, context): 
    # Getting the S3 bucket and key from the event but in this case we will use the sample image dataset/(Please input the directory where you keeping your data). 
    sample_images = r"Sample Image Data Set\Sample Image Data Set"


    # Debugging path
    if not os.path.exists(sample_images):
        print(f"Directory not found: {sample_images}")
        return {
            'statusCode': 404,
            'body': f"Directory not found: {sample_images}"
        }
    
    all_files = os.listdir(sample_images)
    print(f"All files in directory: {all_files}")

    #Listing all jpg files in the sample dir
    image_files = [f for f in all_files if f.lower().endswith('.jpg')]
    print(f"JPG files found: {image_files}")

    results = [] 

    # Fetching the image path so I can access sample images. 
    for image in image_files: 
        image_path = os.path.join(sample_images, image)
        vector = encode_image(image_path)


        if vector is not None:
        #Adding the vector to my results list
            results.append({
                "image_key": image_files,
                "vector": vector
            })

    return {
        'statusCode': 200, 
        'body': results
    }

# Testing the sampled images 
if __name__ == "__main__": 
    result = lambda_handler(None, None)
    print(result)