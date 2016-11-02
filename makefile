SRC_DIR     = $(realpath ./)
INSTALL_DIR = $(realpath /home/$(USER)/bin/)
SCRIPTS     = $(wildcard $(SRC_DIR)/*sh)
TARGETS     = $(INSTALL_DIR)/$(notdir $(basename $(SCRIPTS)))

all : $(TARGETS)

% : %.sh
	ln -s $^ $@ 

uninstall :
	rm $(TARGETS)