# Array of all benchmarks that require configure before make:
# Skipped: network benchmarks, office/ghostscript, 
declare -a config_dirs=( 
	"consumer/tiff-v3.5.4" 
	"consumer/mad/mad-0.14.2b" 
	"consumer/jpeg/jpeg-6a" 
	"office/rsynth" 
	"office/sphinx" 
	 )

# All paths:
declare -a make_dirs=(
	"consumer/tiff-v3.5.4"
	"consumer/mad/mad-0.14.2b"
	# "consumer/jpeg/jpeg-6a"
	# "office/ispell"
	# "office/rsynth"
	# # Sphinx may need to be fixed for compilation
	# "office/sphinx"
	# "office/stringsearch"
	# "security/blowfish"
	# "security/pgp/src"
	# # PGP may have linker errors, also requires target arm-linux
	# "security/rijndael"
	# "security/sha"
	# # adpcm places execs in bin file (above src)
	# "telecomm/adpcm/src"
	# "telecomm/CRC32/"
	# "telecomm/FFT"
	# "telecomm/gsm"
	)

BASE_DIR=$(pwd)

echo "CONFIGURING:"

for dir in "${config_dirs[@]}"
do
	echo $dir
	cd $dir
	pwd
	./configure --host=arm > /dev/null
	cd $BASE_DIR
	pwd
done

echo "MAKING:";

for dir in "${make_dirs[@]}"
do
	echo $dir
	cd $dir
	make clean 	> /dev/null
	make 		> /dev/null
	cd $BASE_DIR
done
