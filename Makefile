PREFIX = /usr
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share
MANDIR = $(DATADIR)/man
LICENSEDIR = $(DATADIR)/license

PKGNAME = blue
COMMAND = blue

all:
clean:

install: install-cmd install-doc install-license
install-doc: install-man

install-cmd:
	mkdir -p -- "$(DESTDIR)$(BINDIR)"
	cp -- blue.py "$(DESTDIR)$(BINDIR)/$(COMMAND)"
	chmod 0755 -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"

install-man:
	mkdir -p -- "$(DESTDIR)$(MANDIR)/man1"
	cp -- blue.py "$(DESTDIR)$(MANDIR)/man1/$(COMMAND).1"
	chmod 0644 -- "$(DESTDIR)$(MANDIR)/man1/$(COMMAND).1"

install-license:
	mkdir -p -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	cp -- LICENSE "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/LICENSE"
	chmod 0644 -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/LICENSE"

uninstall:	
	-rm -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"
	-rm -- "$(DESTDIR)$(MANDIR)/man1/$(COMMAND).1"
	-rm -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/LICENSE"
	-rmdir -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"

.PHONY: all install uninstall clean
.PHONY: install-cmd install-doc install-man install-license
