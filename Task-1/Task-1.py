def caesar_cipher(text, shift, mode):
    result = ""

    for char in text:
        if char.isalpha():  # Check if it's a letter
            base = ord('A') if char.isupper() else ord('a')
            if mode == 'encrypt':
                result += chr((ord(char) - base + shift) % 26 + base)
            elif mode == 'decrypt':
                result += chr((ord(char) - base - shift) % 26 + base)
        else:
            # Non-alphabetic characters remain unchanged
            result += char

    return result


def main():
    print("🔐 Caesar Cipher - Encrypt & Decrypt Tool")
    print("-----------------------------------------")

    mode = input("Choose mode (encrypt/decrypt): ").strip().lower()
    if mode not in ['encrypt', 'decrypt']:
        print("❌ Invalid mode. Please choose 'encrypt' or 'decrypt'.")
        return

    message = input("Enter your message: ")
    try:
        shift = int(input("Enter shift value (0-25): "))
    except ValueError:
        print("❌ Please enter a valid number for shift.")
        return

    if not (0 <= shift <= 25):
        print("❌ Shift must be between 0 and 25.")
        return

    result = caesar_cipher(message, shift, mode)

    print(f"\n✅ Result ({mode}ed message): {result}")


if __name__ == "__main__":
    main()
