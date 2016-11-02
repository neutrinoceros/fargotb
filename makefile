SRC_DIR     = $(realpath ./)
INSTALL_DIR = $(realpath /home/$(USER)/bin/)
SCRIPTS     = $(wildcard $(SRC_DIR)/*sh)
TARGETS     = $(addprefix $(INSTALL_DIR)/, $(basename $(notdir $(SCRIPTS))))

all : $(TARGETS)

% : %.sh
	ln -s $^ $@ 

uninstall :
	rm $(TARGETS)