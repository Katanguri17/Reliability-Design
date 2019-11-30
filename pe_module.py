import array
import pefile
import math
import os

# credits http://n10info.blogspot.com/2014/06/entropy-and-distinctive-signs-of-packed.html
def entropy(data):
    entropy = 0
    occurrences = array.array('f', [0] * 256)
    for x in data:
        occurrences[x] += 1
    for x in occurrences:
        temp = float(x) / len(data)
        if temp:
            entropy -= (math.log(temp) / math.log(2)) * x
    entropy /= len(data)
    return entropy


def get_pe_credentials(exe_file_path):
    file = pefile.PE(exe_file_path, fast_load=True)
    credentials = []
    # ----------FILE_HEADER----------
    credentials.append(file.FILE_HEADER.Machine)
    credentials.append(file.FILE_HEADER.NumberOfSections)
    credentials.append(file.FILE_HEADER.TimeDateStamp)
    credentials.append(file.FILE_HEADER.PointerToSymbolTable)
    credentials.append(file.FILE_HEADER.NumberOfSymbols)
    credentials.append(file.FILE_HEADER.SizeOfOptionalHeader)
    credentials.append(file.FILE_HEADER.Characteristics)
    # ----------OPTIONAL_HEADER----------
    credentials.append(file.OPTIONAL_HEADER.Magic)
    credentials.append(file.OPTIONAL_HEADER.MajorLinkerVersion)
    credentials.append(file.OPTIONAL_HEADER.MinorLinkerVersion)
    credentials.append(file.OPTIONAL_HEADER.SizeOfCode)
    credentials.append(file.OPTIONAL_HEADER.SizeOfInitializedData)
    credentials.append(file.OPTIONAL_HEADER.SizeOfUninitializedData)
    credentials.append(file.OPTIONAL_HEADER.AddressOfEntryPoint)
    credentials.append(file.OPTIONAL_HEADER.BaseOfCode)
    credentials.append(file.OPTIONAL_HEADER.BaseOfData)
    credentials.append(file.OPTIONAL_HEADER.ImageBase)
    credentials.append(file.OPTIONAL_HEADER.SectionAlignment)
    credentials.append(file.OPTIONAL_HEADER.FileAlignment)
    credentials.append(file.OPTIONAL_HEADER.MajorOperatingSystemVersion)
    credentials.append(file.OPTIONAL_HEADER.MinorOperatingSystemVersion)
    credentials.append(file.OPTIONAL_HEADER.MajorImageVersion)
    credentials.append(file.OPTIONAL_HEADER.MinorImageVersion)
    credentials.append(file.OPTIONAL_HEADER.MajorSubsystemVersion)
    credentials.append(file.OPTIONAL_HEADER.MinorSubsystemVersion)
    credentials.append(file.OPTIONAL_HEADER.Reserved1)
    credentials.append(file.OPTIONAL_HEADER.SizeOfImage)
    credentials.append(file.OPTIONAL_HEADER.SizeOfHeaders)
    credentials.append(file.OPTIONAL_HEADER.CheckSum)
    credentials.append(file.OPTIONAL_HEADER.Subsystem)
    credentials.append(file.OPTIONAL_HEADER.DllCharacteristics)
    credentials.append(file.OPTIONAL_HEADER.SizeOfStackReserve)
    credentials.append(file.OPTIONAL_HEADER.SizeOfStackCommit)
    credentials.append(file.OPTIONAL_HEADER.SizeOfHeapReserve)
    credentials.append(file.OPTIONAL_HEADER.SizeOfHeapCommit)
    credentials.append(file.OPTIONAL_HEADER.LoaderFlags)
    credentials.append(file.OPTIONAL_HEADER.NumberOfRvaAndSizes)
    # ----------PE Sections----------
    # print(credentials)
    credentials.append(len(file.sections))
    # TODO entropy
    return credentials
def get_csv(path):
    file = "data.csv"
    csv_seperator = "|"


    columns = [
        "Name",
        "md5",
        "Machine",
        "NumberOfSections",
        "TimeDateStamp",
        "PointerToSymbolTable",
        "NumberOfSymbols",
        "SizeOfOptionalHeader",
        "Characteristics",
        "Magic",
        "MajorLinkerVersion",
        "MinorLinkerVersion",
        "SizeOfCode",
        "SizeOfInitializedData",
        "SizeOfUninitializedData",
        "AddressOfEntryPoint",
        "BaseOfCode",
        "BaseOfData",
        "ImageBase",
        "SectionAlignment",
        "FileAlignment",
        "MajorOperatingSystemVersion",
        "MinorOperatingSystemVersion",
        "MajorImageVersion",
        "MinorImageVersion",
        "MajorSubsystemVersion",
        "MinorSubsystemVersion",
        "SizeOfImage",
        "SizeOfHeaders",
        "CheckSum",
        "Subsystem",
        "DllCharacteristics",
        "SizeOfStackReserve",
        "SizeOfStackCommit",
        "SizeOfHeapReserve",
        "SizeOfHeapCommit",
        "LoaderFlags",
        "NumberOfRvaAndSizes",
    ]
    csv_file = open(file, "a")
    csv_file.write(csv_seperator.join(columns) + "\n")
    data = get_pe_credentials(path)
    csv_file.write(csv_seperator.join(map(lambda x: str(x), data)) + "\n")