
TARGET = hello

SRCS = hello.c

OBJS = $(SRCS:.c=.o)

.PHONY:	all
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
