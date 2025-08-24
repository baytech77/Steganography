from PIL import Image
from cryptography.fernet import Fernet, InvalidToken
import base64
import hashlib


SIGNATURE = "StegoApp: \n\n"

def key_generation(password: str) -> bytes:
    # Deriving a key from password using SHA-256
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())


def encrypt_message(message:str, password:str) -> str:
    key = key_generation(password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(message.encode())
    return encrypted.decode() # help to convert byte to string for embedding the message


def decrypt_message(encrypted_message: str, password:str) -> str:
    try:
        key = key_generation(password)
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_message.encode())
        return decrypted.decode()
    except InvalidToken:
        return None


def binary_converter(data):
    """
    convert input data to binary string,
    supports str, bytes/bytearray and int.
    """
    if isinstance(data, str):
        return "".join([format(ord(i), '08b') for i in data])
    elif isinstance(data, (bytes, bytearray)):
        return [format(i, '08b') for i in data]
    elif isinstance(data, int):
        return format(data, '08b')
    else:
        raise TypeError("Input type not supported: must be string, bytes, bytearray or int !!")
    
def encode_image(image, secret_message, password):
    """
    Encoding a secret message into the image using LSB method
    """

    # encrpte message with password before adding signature
    encrypted_message = encrypt_message(secret_message, password)
    if encrypted_message == None:
        raise ValueError("Encryption failed!!")
    
    message_with_signature = SIGNATURE + encrypted_message
    binary_message = binary_converter(message_with_signature) + "1111111111111110" # helps to mark the end of the embedded data  
    data_index = 0
    img = image.convert('RGB')
    pixels = list(img.getdata())
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel
        if data_index < len(binary_message):
            r = (r & ~1) | int(binary_message[data_index])
            data_index += 1
        if data_index < len(binary_message):
            g = (g & ~1) | int(binary_message[data_index])
            data_index += 1
        if data_index < len(binary_message):
            b = (b & ~1) | int(binary_message[data_index])
            data_index += 1
        new_pixels.append((r,g,b))
    
    img.putdata(new_pixels)
    return img


def decode_image2(image: Image.Image, password: str = None, check_only: bool = False):
    img = image.convert('RGB')
    binary_data = ""

    for pixel in img.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)

    # To detect images not encoded by this app
    delimeter = "1111111111111110"
    # check if delimeter exit in the binary data of the image
    delimeter_index = binary_data.find(delimeter)
    if delimeter_index == -1:
        return None, "This image is not encoded by this app"
    
    relevant_data = binary_data[:delimeter_index]

    all_bytes = [relevant_data[i:i+8] for i in range(0, len(relevant_data), 8)]
    decoded_message = "".join(chr(int(byte, 2)) for byte in all_bytes)

    if not decoded_message.startswith(SIGNATURE):
        return None, "This image is not encoded by this app!!"
    
    if check_only:
        return "",  None
    
    if password == None:
        return None, "password is required"
    
    encrypted_message = decoded_message[len(SIGNATURE):]
    secret_message = decrypt_message(encrypted_message, password)

    if secret_message == None:
        return None, "Password does not match!!"
    
    return secret_message, None

def decode_image(image: Image.Image, password=None, check_only=False):
    """
    Decode and extract the hidden message 
    from the image using LSB.
    """
    img = image.convert('RGB')
    binary_data = ""

    for pixel in img.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)

    # To detect images not encoded by this app
    delimeter = "1111111111111110"
    # check if delimeter exit in the binary data of the image
    delimeter_index = binary_data.find(delimeter)
    if delimeter_index == -1:
        return None, "This image is not encoded by this app"
    
    relevant_data = binary_data[:delimeter_index]

    all_bytes = [relevant_data[i:i+8] for i in range(0, len(relevant_data), 8)]
    decoded_message = "".join(chr(int(byte, 2)) for byte in all_bytes)
    
    #for byte in all_bytes:
    #    if byte == '11111111': # delimeter to mark the end of message
    #        break
    #    decoded_message += chr(int(byte, 2))
    if not decoded_message.startswith(SIGNATURE):
        return None, "This image is not encoded by this app!!"
    encrypted_message = decoded_message[len(SIGNATURE):]
    secret_message = decrypt_message(encrypted_message, password)
    if secret_message == None:
        return None, "Password does not match!!"
    
    return secret_message, None
        