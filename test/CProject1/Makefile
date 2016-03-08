CFLAGS=-Wall -g3

all: hs

hs: hs.o hs_util.o
	gcc $(CFLAGS) -o hs hs.o hs_util.o

hs.o: hs.c
	gcc $(CFLAGS) -c hs.c

hs_util.o: hs_util.c
	gcc $(CFLAGS) -c hs_util.c

clean:
	rm hs *.o
