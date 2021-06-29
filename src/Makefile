all: sttalben_sqlist

CC=g++
CFLAGS=$(shell /usr/bin/pkg-config --cflags gtkmm-3.0 sqlite3)
LDFLAGS=$(shell /usr/bin/pkg-config --libs gtkmm-3.0 sqlite3)

%.o:%.cc
	$(CC) -g -Wall -c $(CFLAGS) $< -o $@


sttalben_sqlist: main.o mywin.o dbsqlite3.o
	$(CC) $(LDFLAGS) $^ -o $@
