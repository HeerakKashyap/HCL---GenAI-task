import os
import sys

def main():
    print("RAG-Powered Assistant - Setup and Run")
    print("=" * 50)
    
    if not os.path.exists('.env'):
        print("\nCreating .env file from template...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as f:
                content = f.read()
            with open('.env', 'w') as f:
                f.write(content)
            print("Created .env file. Please add your OPENAI_API_KEY if you want to use cloud features.")
        else:
            print("Warning: .env.example not found")
    
    print("\nSetting up directories...")
    os.system('python setup.py')
    
    if not os.path.exists('documents') or len(os.listdir('documents')) == 0:
        print("\nNo documents found in documents/ directory.")
        print("Copying sample document...")
        if os.path.exists('sample_document.txt'):
            import shutil
            if not os.path.exists('documents'):
                os.makedirs('documents')
            shutil.copy('sample_document.txt', 'documents/sample_document.txt')
            print("Sample document copied to documents/")
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    print("\nTo start the backend server:")
    print("  python app.py")
    print("\nTo start the frontend (in another terminal):")
    print("  cd client && npm start")
    print("\nMake sure to add your documents to the documents/ directory")

if __name__ == '__main__':
    main()

