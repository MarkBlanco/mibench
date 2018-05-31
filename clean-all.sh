# All paths:
declare -a make_dirs=(
	"consumer/tiff-v3.5.4"
	"consumer/mad/mad-0.14.2b"
	"consumer/jpeg/jpeg-6a"
	"office/ispell"
	"office/rsynth"
	# Sphinx may need to be fixed for compilation
	"office/sphinx"
	"office/stringsearch"
	"security/blowfish"
	"security/pgp/src"
	# PGP may have linker errors, also requires target arm-linux
	"security/rijndael"
	"security/sha"
	# adpcm places execs in bin file (above src)
	"telecomm/adpcm/src"
	"telecomm/CRC32/"
	"telecomm/FFT"
	"telecomm/gsm"
	)

BASE_DIR=$(pwd)

echo "CLEANING:";

for dir in "${make_dirs[@]}"
do
	echo $dir
	cd $dir
	make clean 	
	cd $BASE_DIR
done
