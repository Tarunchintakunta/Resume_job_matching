import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    
    for line in process.stdout:
        print(line.strip())
    
    process.wait()
    return process.returncode

def setup_backend():
    """Set up the backend environment and prepare everything"""
    print("Setting up backend environment...")
    
    # Create directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("scripts", exist_ok=True)
    
    # Run data preparation script
    print("\n=== Preparing datasets ===")
    if run_command("python scripts/prepare_data.py") != 0:
        print("Error: Failed to prepare datasets")
        return False
    
    # Run model training script
    print("\n=== Training models ===")
    if run_command("python scripts/train_model.py") != 0:
        print("Error: Failed to train models")
        return False
    
    # Set up MongoDB
    print("\n=== Setting up MongoDB ===")
    if run_command("python scripts/setup_mongodb.py") != 0:
        print("Error: Failed to set up MongoDB")
        return False
    
    print("\n=== Backend setup completed! ===")
    print("You can now run the API server with: python main.py")
    return True

if __name__ == "__main__":
    setup_backend()