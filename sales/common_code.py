
import hashlib
import os

def generate_file_hash(file_path, hash_algorithm='md5'):
    # Initialize the hash algorithm (e.g., sha256, md5, sha1)
    try:
        hash_algo = hashlib.new(hash_algorithm)
    except ValueError:
        raise ValueError(f'Unsupported hash type: {hash_algorithm}')
    
    # Open the file in binary mode and read in chunks
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):  # Read the file in chunks of 8KB
            hash_algo.update(chunk)
    
    # Return the hexadecimal digest of the hash
    return hash_algo.hexdigest()

def get_readable_file_size(size_in_bytes):
    size_units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    size_index = 0

    while size_in_bytes >= 1024 and size_index < len(size_units) - 1:
        size_in_bytes /= 1024
        size_index += 1

    return f"{size_in_bytes:.2f} {size_units[size_index]}"

def list_directory(path):
        file_info = []

        if not os.path.exists(path):
            raise ValueError(f"The provided path '{path}' does not exist.")
        
        if not os.path.isdir(path):
            raise ValueError(f"The provided path '{path}' is not a directory.")
        
        for subdirectory in os.listdir(path):
            subdirectory_path = os.path.join(path, subdirectory)
            
            if os.path.isdir(subdirectory_path):  # Check if it's a directory
                for filename in os.listdir(subdirectory_path):
                    file_path = os.path.join(subdirectory_path, filename)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        file_info.append({'name': filename, 'size': get_readable_file_size(file_size)})

        return file_info