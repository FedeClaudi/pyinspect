path="../media/${1}"

echo "Converting ${path}"
terminalizer render $path -o $path

echo "Extracting"
python get_gif_last_frame.py "${path}.gif"