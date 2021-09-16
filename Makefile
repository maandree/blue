.POSIX:

CONFIGFILE = config.mk
include $(CONFIGFILE)


all:
	@:

install:
	mkdir -p -- "$(DESTDIR)$(PREFIX)/bin"
	mkdir -p -- "$(DESTDIR)$(MANPREFIX)/man1"
	cp -- blue "$(DESTDIR)$(PREFIX)/bin/"
	cp -- blue.1 "$(DESTDIR)$(MANPREFIX)/man1/"

uninstall:
	-rm -f -- "$(DESTDIR)$(PREFIX)/bin/blue"
	-rm -f -- blue.1 "$(DESTDIR)$(MANPREFIX)/man1/blue.1"

clean:
	@:

.PHONY: all install uninstall clean
