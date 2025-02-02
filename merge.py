# Merge Moraea's generated binaries with PatcherSupportPkg format
# Usage: python merge.py --version <OS version> --input <input folder>

import argparse
import subprocess
from pathlib import Path

class moraea_binary_merging:

    def __init__(self, version, input_folder):
        self.version = self.convert_os_to_kernel(version)
        self.file_map = self.generate_file_map(self.version)

        self.input_folder = Path(input_folder)
        if not self.input_folder.exists():
            print("Input folder does not exist")
            exit(1)

        self.update_binaries()


    def convert_os_to_kernel(self, version):
        try:
            version = int(version)
        except ValueError:
            print("Invalid OS version")
            exit(1)

        if version >= 11:
            version =  version + 9
            print(f"  - Adjusted Kernel version to {version}")
            return str(version)
        raise ValueError("Invalid OS version, only 11+ supported")


    def generate_file_map(self, version):
        FILE_MAP = {
            "Cass2": {
                "IOAccelerator":          f"Universal-Binaries/10.13.6-{version}/System/Library/PrivateFrameworks/IOAccelerator.framework/Versions/A/IOAccelerator",
                "IOAcceleratorOld.dylib": f"Universal-Binaries/10.13.6-{version}/System/Library/PrivateFrameworks/IOAccelerator.framework/Versions/A/IOAcceleratorOld.dylib",
                "IOSurface":              f"Universal-Binaries/10.14.6-{version}/System/Library/Frameworks/IOSurface.framework/Versions/A/IOSurface",
                "IOSurfaceOld.dylib":     f"Universal-Binaries/10.14.6-{version}/System/Library/Frameworks/IOSurface.framework/Versions/A/IOSurfaceOld.dylib",
            },
            "Common": {
                "CoreDisplay":          f"Universal-Binaries/10.14.4-{version}/System/Library/Frameworks/CoreDisplay.framework/Versions/A/CoreDisplay",
                "CoreDisplayOld.dylib": f"Universal-Binaries/10.14.4-{version}/System/Library/Frameworks/CoreDisplay.framework/Versions/A/CoreDisplayOld.dylib",
                "QuartzCore":           f"Universal-Binaries/10.15.7-{version}/System/Library/Frameworks/QuartzCore.framework/Versions/A/QuartzCore",
                "QuartzCoreOld.dylib":  f"Universal-Binaries/10.15.7-{version}/System/Library/Frameworks/QuartzCore.framework/Versions/A/QuartzCoreOld.dylib",
                "SkyLight":             f"Universal-Binaries/10.14.6-{version}/System/Library/PrivateFrameworks/SkyLight.framework/Versions/A/SkyLight",
                "SkyLightOld.dylib":    f"Universal-Binaries/10.14.6-{version}/System/Library/PrivateFrameworks/SkyLight.framework/Versions/A/SkyLightOld.dylib",
            },
            "Zoe": {
                "IOSurface":          f"Universal-Binaries/10.15.7-{version}/System/Library/Frameworks/IOSurface.framework/Versions/A/IOSurface",
                "IOSurfaceOld.dylib": f"Universal-Binaries/10.15.7-{version}/System/Library/Frameworks/IOSurface.framework/Versions/A/IOSurfaceOld.dylib",
            },
        }

        return FILE_MAP

    def update_binaries(self):
        print(f"- Processing files against version: {self.version}")
        for folder in self.file_map:
            for binary in self.file_map[folder]:
                print(f"  - Processing binary: {binary} ({folder})")

                # Check if exists at source location
                if not Path(self.input_folder / f"{folder}/{binary}").exists():
                    print("    - Binary not found at source location, skipping")
                    continue

                # Check if exists at destination location
                if Path(self.file_map[folder][binary]).exists():
                    print("    - Binary found at destination location, removing")
                    subprocess.run(["rm", self.file_map[folder][binary]])

                # Copy binary to destination location
                print("    - Copying binary to destination location")
                subprocess.run(["cp", self.input_folder / f"{folder}/{binary}", self.file_map[folder][binary]])


if __name__ == "__main__":
    print("- Starting Moraea Merging Script")

    parser = argparse.ArgumentParser()
    # 2 arguments each with a value
    parser.add_argument("--version", type=str, help="OS version")
    parser.add_argument("--input", type=str, help="Input folder")
    args = parser.parse_args()

    if not args.version or not args.input:
        print("Missing arguments:")
        if not args.version:
            print("  --version")
        if not args.input:
            print("  --input")
        exit(1)

    moraea_binary_merging(args.version, args.input)

    print("- Done")