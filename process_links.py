import re
import sys
from collections import defaultdict

# De-duplicates image links, saving only the original if possible, and falling back to the biggest resized option if needed
def process_links(filename):
    # Read the input text file
    with open(filename, 'r') as file:
        links = file.readlines()

    # Process the links
    image_links = defaultdict(dict)
    non_image_links = []
    original_images = set()

    for link in links:
        link = link.strip()
        match = re.match(r'(.*?)(\d+x\d+)?(\.(jpg|jpeg|bmp|gif|png|webp))$', link)

        if match:
            prefix, size, ext = match.group(1), match.group(2), match.group(3)

            if size:
                width, height = map(int, size.split('x'))

                # Store the image link with the largest size
                if prefix not in image_links or (width * height) > (image_links[prefix][1] * image_links[prefix][2]):
                    image_links[prefix] = (link, width, height)
            else:
                original_images.add(prefix)
        else:
            non_image_links.append(link)

    # Remove resized images if there is an original non-prefixed version
    for prefix in original_images:
        image_links.pop(prefix, None)

    # Combine the de-duplicated image links and non-image links
    result_links = [data[0] for data in image_links.values()] + list(original_images) + non_image_links

    # Write the output to a text file
    output_filename = f'output_{filename}'
    with open(output_filename, 'w') as file:
        for link in result_links:
            file.write(link + '\n')

    print(f"De-duplicated links are saved in '{output_filename}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input filename as a command-line argument.")
    else:
        input_filename = sys.argv[1]
        process_links(input_filename)
