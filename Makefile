SUBDIRS:=$(wildcard *-*/.)

all: $(SUBDIRS)

$(SUBDIRS):
	+$(MAKE) -C $@

.PHONY: all $(SUBDIRS)

clean:
	for dir in $(SUBDIRS); do (cd $$dir; make clean || exit 1) || exit 1; done
