import os
import shutil

def ensure_index_php(root_dir, template_file):
    """
    Walk through subdirectories of root_dir.
    If index.php is missing, copy template_file as index.php.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip the root if you don't want index.php there
        if "index.php" not in filenames:
            target = os.path.join(dirpath, "index.php")
            shutil.copy(template_file, target)
            print(f"Created: {target}")
        else:
            print(f"Already exists: {os.path.join(dirpath, 'index.php')}")

if __name__ == "__main__":
    # change these paths
    ROOT_DIR = "/eos/user/s/sgiappic/www/Higgs_xsec/"         # root directory to walk
    TEMPLATE_FILE = "/eos/user/s/sgiappic/www/index.php"  # template index.php to copy
    
    ensure_index_php(ROOT_DIR, TEMPLATE_FILE)
