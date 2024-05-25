from PIL import Image

# Open the image file
img_path = '20240303202705.png'
img = Image.open(img_path)

# Define the size of each avatar within the grid (assumption based on visual inspection)
# The grid seems to have a uniform distribution of avatars
avatar_width = img.width // 6
avatar_height = img.height // 5

# Create a list to store file paths of cropped avatars
avatar_file_paths = []

# Loop through the grid and crop out each avatar
for row in range(5):
    for col in range(6):
        # Calculate the bounds of the current avatar
        left = col * avatar_width
        top = row * avatar_height
        right = left + avatar_width
        bottom = top + avatar_height
        # Crop the current avatar
        avatar = img.crop((left, top, right, bottom))
        
        # Save the cropped avatar to a file
        avatar_file_path = f'./data/avatar_{row}_{col}.png'
        avatar.save(avatar_file_path)
        avatar_file_paths.append(avatar_file_path)

# Output the file paths of the saved avatars
avatar_file_paths
