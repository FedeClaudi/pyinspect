cd "../media"

src="${1}.gif"
dst1="${1}_trim.gif"
dst="${1}_cut.gif"

echo "trimming ${src} [${2}->${3}] and saving to ${dst}"


# first trim
echo "trimming"
gifsicle $src "#${2}-${3}" --colors 256 > $dst1

# then add a delay to the end
echo "adding delay"
gifsicle "#0--2" -d200 "#-1"< $dst1 > $dst
rm $dst1

cd "../scripts"
echo "done!"