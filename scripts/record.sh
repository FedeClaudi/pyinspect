
cd '../media'
terminalizer record $1 -c "config.yml" -k

cd '../scripts'

# Convert
bash convert_save_gif.sh $1

