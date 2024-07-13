import asyncio
import aiofiles
import os
import shutil
import argparse
from pathlib import Path
from collections import defaultdict

def parse_arguments():
    parser = argparse.ArgumentParser(description="Sort files by extension asynchronously.")
    parser.add_argument("source_folder", type=str, help="Source folder to read files from.")
    parser.add_argument("output_folder", type=str, help="Output folder to save sorted files.")
    return parser.parse_args()

async def create_output_directories(output_folder, extensions):
    for ext in extensions:
        ext_folder = os.path.join(output_folder, ext.lstrip('.'))
        if not os.path.exists(ext_folder):
            os.makedirs(ext_folder)

async def read_folder(source_folder):
    files = []
    for root, _, filenames in os.walk(source_folder):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

async def copy_file(file_path, output_folder):
    ext = Path(file_path).suffix
    async with aiofiles.open(file_path, 'rb') as f:
        content = await f.read()
    dest_folder = os.path.join(output_folder, ext.lstrip('.'))
    dest_path = os.path.join(dest_folder, os.path.basename(file_path))
    async with aiofiles.open(dest_path, 'wb') as f:
        await f.write(content)

async def main():
    args = parse_arguments()
    source_folder = args.source_folder
    output_folder = args.output_folder

    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    files = await read_folder(source_folder)
    extensions = {Path(file).suffix for file in files}

    await create_output_directories(output_folder, extensions)

    tasks = [copy_file(file, output_folder) for file in files]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
    
                