FILE = bitcnt_1.c bitcnt_2.c bitcnt_3.c bitcnt_4.c bitcnts.c bitfiles.c bitstrng.c bstr_i.c 

.PHONY: bitcnts

bitcnts: ${FILE} Makefile
	gcc -static ${FILE} -O3 -o automotive-bitcounts

clean:
	rm -rf automotive-bitcnts output*
