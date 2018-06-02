SUBDIRS:=$(wildcard */.)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

.PHONY: all $(SUBDIRS)

clean:
	$(MAKE) clean -C $(SUBDIRS)
