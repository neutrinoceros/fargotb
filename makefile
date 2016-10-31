SRC         = $(realpath ./)
script      = $(SRC)/slaughter.sh
INSTALL_DIR = $(realpath /home/$(USER)/bin/)
TARGET      = $(INSTALL_DIR)/slaughter
FLAGS	    = -s

all : $(TARGET)

$(TARGET) : $(script)
	ln $(FLAGS) $^ $@ 

clean :
	rm *~
	rm $(TARGET)