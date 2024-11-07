import os
import pandas as pd
import requests

# Load the metadata
metadata = pd.read_csv('gulf_of_mexico.csv')  # Replace with your actual CSV file path

# Create the main dataset directory
main_dir = 'organized_fish_dataset'
os.makedirs(main_dir, exist_ok=True)

# Dictionary to maintain counters for each species
species_counters = {}

# Loop through each row in the metadata
for index, row in metadata.iterrows():
    species_name = str(row['common_name'])  # You can change this to 'Scientific Name' if preferred
    image_url = row['image_url']  # Make sure this column exists in your CSV

    # Create a species folder if it doesn't exist
    species_folder = os.path.join(main_dir, species_name.replace(" ", "_"))  # Replace spaces with underscores for folder names
    os.makedirs(species_folder, exist_ok=True)

    # Define the image file name
    if pd.notna(image_url):  # Check if the image_url is not empty
        # Get the original filename and extension
        original_filename = os.path.basename(image_url)
        name, ext = os.path.splitext(original_filename)  # Split filename into name and extension
        
        # Initialize the counter for the species if it doesn't exist
        if species_name not in species_counters:
            species_counters[species_name] = 0
        
        # Create a unique image name based on species name and species-specific index, preserving original extension
        image_name = f"{species_name.replace(' ', '_')}_{species_counters[species_name]}{ext}"  # Use original extension
        
        # Increment the counter for the species
        species_counters[species_name] += 1
        
        image_path = os.path.join(species_folder, image_name)

        # Download the image
        try:
            img_data = requests.get(image_url).content
            with open(image_path, 'wb') as handler:
                handler.write(img_data)
            print(f'Downloaded: {image_name} to {species_folder}')
        except Exception as e:
            print(f'Error downloading {image_url}: {e}')

print("All images have been downloaded and organized.")