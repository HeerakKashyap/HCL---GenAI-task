import os
import shutil

def setup_directories():
    directories = [
        'documents',
        'vector_store',
        'documents/processed'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory exists: {directory}")

if __name__ == '__main__':
    setup_directories()
    print("Setup complete. Add PDF or TXT files to the 'documents' directory.")

