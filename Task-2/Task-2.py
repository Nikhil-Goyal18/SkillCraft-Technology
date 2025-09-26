from PIL import Image
import random

def encrypt_image_swap_pixels(image, key):

    pixels = list(image.getdata())
    random.seed(key)
    indices = list(range(len(pixels)))
    random.shuffle(indices)

    encrypted_pixels = [pixels[i] for i in indices]
    encrypted_image = Image.new(image.mode, image.size)
    encrypted_image.putdata(encrypted_pixels)

    return encrypted_image, indices

def decrypt_image_swap_pixels(encrypted_image, indices):

    encrypted_pixels = list(encrypted_image.getdata())
    decrypted_pixels = [None] * len(encrypted_pixels)

    for original_pos, encrypted_pos in enumerate(indices):
        decrypted_pixels[encrypted_pos] = encrypted_pixels[original_pos]

    decrypted_image = Image.new(encrypted_image.mode, encrypted_image.size)
    decrypted_image.putdata(decrypted_pixels)

    return decrypted_image

def encrypt_image_shift_pixels(image, shift):
    def shift_pixel(pixel):
        return tuple((value + shift) % 256 for value in pixel)

    pixels = list(image.getdata())
    shifted_pixels = [shift_pixel(pixel) for pixel in pixels]

    encrypted_image = Image.new(image.mode, image.size)
    encrypted_image.putdata(shifted_pixels)

    return encrypted_image

def decrypt_image_shift_pixels(encrypted_image, shift):
    
    def unshift_pixel(pixel):
        return tuple((value - shift) % 256 for value in pixel)

    pixels = list(encrypted_image.getdata())
    unshifted_pixels = [unshift_pixel(pixel) for pixel in pixels]

    decrypted_image = Image.new(encrypted_image.mode, encrypted_image.size)
    decrypted_image.putdata(unshifted_pixels)

    return decrypted_image

def main():
    print("Simple Image Encryption Tool using Pixel Manipulation")
    print("-----------------------------------------------------")

    filepath = input("Enter path to the image file (e.g., image.png): ").strip()
    try:
        image = Image.open(filepath)
        if image.mode != 'RGB':
            image = image.convert('RGB')  # Ensure image is RGB
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    operation = input("Choose operation (encrypt/decrypt): ").strip().lower()
    if operation not in ['encrypt', 'decrypt']:
        print("Invalid operation. Choose 'encrypt' or 'decrypt'.")
        return

    method = input("Choose method (swap/shift): ").strip().lower()
    if method not in ['swap', 'shift']:
        print("Invalid method. Choose 'swap' or 'shift'.")
        return

    if method == 'swap':
        key = input("Enter a secret key (any string) for pixel swapping: ").strip()
        if operation == 'encrypt':
            encrypted_image, indices = encrypt_image_swap_pixels(image, key)
            encrypted_image.save('encrypted_swap.png')
            # Save the permutation for decryption
            with open('swap_indices.txt', 'w') as f:
                f.write(','.join(map(str, indices)))
            print("Image encrypted with pixel swapping and saved as 'encrypted_swap.png'.")
            print("Permutation indices saved as 'swap_indices.txt' for decryption.")
        else:
            # For decryption, load permutation indices
            try:
                with open('swap_indices.txt', 'r') as f:
                    indices = list(map(int, f.read().split(',')))
                decrypted_image = decrypt_image_swap_pixels(image, indices)
                decrypted_image.save('decrypted_swap.png')
                print("Image decrypted and saved as 'decrypted_swap.png'.")
            except Exception as e:
                print(f"Error reading permutation indices: {e}")
                return

    else:  # method == 'shift'
        try:
            shift = int(input("Enter shift value (integer 0-255): "))
            if not (0 <= shift <= 255):
                print("Shift must be between 0 and 255.")
                return
        except ValueError:
            print("Invalid shift value. Please enter an integer.")
            return

        if operation == 'encrypt':
            encrypted_image = encrypt_image_shift_pixels(image, shift)
            encrypted_image.save('encrypted_shift.png')
            print("Image encrypted by shifting pixel values and saved as 'encrypted_shift.png'.")
        else:
            decrypted_image = decrypt_image_shift_pixels(image, shift)
            decrypted_image.save('decrypted_shift.png')
            print("Image decrypted by reversing pixel shift and saved as 'decrypted_shift.png'.")

if __name__ == "__main__":
    main()
