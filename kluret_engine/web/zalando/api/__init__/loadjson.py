import os

# Define the target directory
directory = r"C:\Users\elias\OneDrive\Desktop\usbaiTraining\usbai_client\kluret_engine\web\zalando\pipline1\__link__"

# Ensure the directory exists
if not os.path.exists(directory):
    os.makedirs(directory)

# Create 10 files starting from z3.json to z12.json
for i in range(1, 10):
    filename = f"__link__{i}.json"
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w') as file:
        file.write('[]')  # Writing an empty JSON object

print(f"Created files from z3.json to z12.json in {directory}")
