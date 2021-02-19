.POSIX:

PREFIX    = /usr
MANPREFIX = $(PREFIX)/share/man

all:
	@:

install:
	mkdir -p -- "$(DESTDIR)$(PREFIX)/bin"
	mkdir -p -- "$(DESTDIR)$(MANPREFIX)/man1"
	mkdir -p -- "$(DESTDIR)$(PREFIX)/share/licenses/blue"
	cp -- blue "$(DESTDIR)$(PREFIX)/bin/"
	cp -- blue.1 "$(DESTDIR)$(MANDIR)/man1/"
	cp -- LICENSE "$(DESTDIR)$(PREFIX)/share/licenses/blue/"

uninstall:
	-rm -f -- "$(DESTDIR)$(PREFIX)/bin/blue"
	-rm -f -- blue.1 "$(DESTDIR)$(MANPREFIX)/man1/blue.1"
	-rm -f -- LICENSE "$(DESTDIR)$(PREFIX)/share/licenses/blue/LICENSE"
	-rmdir -- LICENSE "$(DESTDIR)$(PREFIX)/share/licenses/blue"

clean:
	@:

.PHONY: all install uninstall clean
