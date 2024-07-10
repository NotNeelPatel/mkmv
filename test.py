
def test(output_file_unformatted):
    split_file = output_file_unformatted.split(".")
    if len(split_file) == 1:
        split_file.append("mp4")

    if split_file[-1] != "mp4":
        split_file[-1] = "mp4"
        
    output_file = (".").join(split_file)
    print(output_file)

a = [
    "output",
    "output with spaces",
    "output.mp4",
]

for b in a:
    test(b)