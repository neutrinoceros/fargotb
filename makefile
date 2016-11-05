SRC_DIR     = $(realpath ./)
INSTALL_DIR = $(realpath /home/$(USER)/bin/)
SH_SCRIPTS  = $(wildcard $(SRC_DIR)/*sh)
PY_SCRIPTS  = $(wildcard $(SRC_DIR)/*py)
SH_TARGETS  = $(addprefix $(INSTALL_DIR)/, $(basename $(notdir $(SH_SCRIPTS))))
PY_TARGETS  = $(addprefix $(INSTALL_DIR)/, $(basename $(notdir $(PY_SCRIPTS))))

all : $(SH_TARGETS) $(PY_TARGETS)

$(SH_TARGETS): $(INSTALL_DIR)/% : $(SRC_DIR)/%.sh
	ln -s $^ $@ 

$(PY_TARGETS): $(INSTALL_DIR)/% : $(SRC_DIR)/%.py
	ln -s $^ $@ 

uninstall :
	rm $(SH_TARGETS) $(PY_TARGETS)