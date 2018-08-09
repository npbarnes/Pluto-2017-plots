GENERATED_DIR := generated_plots
EXTERNAL_DIR  := external_plots
LINKS_DIR     := plots

GENERATED_PLOT_NAMES := atmosphere_profile.png xz_context.png shellfeyerabend6.png noshellfeyerabend6.png drape.png synthetic_spectrograms.png \
	wake_structure.png beta_pressure_shell.png beta_pressure_noshell.png
GENERATED_PLOT_PATHS := $(addprefix $(GENERATED_DIR)/,$(GENERATED_PLOT_NAMES))
EXTERNAL_PLOT_NAMES  := mccomasfig7.png heather_scem_espec_no_footer.png mccomasfig6.png
EXTERNAL_PLOT_PATHS  := $(addprefix $(EXTERNAL_DIR)/,$(EXTERNAL_PLOT_NAMES))

ALL_PLOT_NAMES       := $(GENERATED_PLOT_NAMES) $(EXTERNAL_PLOT_NAMES)
ALL_PLOT_PATHS       := $(GENERATED_PLOT_PATHS) $(EXTERNAL_PLOT_PATHS)

ALL_LINKS_PATHS      := $(addprefix $(LINKS_DIR)/,$(ALL_PLOT_NAMES))

.PHONY: all clean

all: $(ALL_LINKS_PATHS)

# All the plots will eventually go into the links directory
# This makes sure that directory exists
$(ALL_PLOT_PATHS): | $(LINKS_DIR)

$(LINKS_DIR):
	mkdir -p $(LINKS_DIR)

# In addition, the generated plots will also go in the generated plots directory
# This makes sure that directory exists
$(GENERATED_PLOT_PATHS): | $(GENERATED_DIR)

$(GENERATED_DIR):
	mkdir -p $(GENERATED_DIR)

# Make the links from every image in generated and external dirs to the cooresponding 
# place in the links directory
$(LINKS_DIR)/%.png: $(GENERATED_DIR)/%.png
	rm -f $(shell pwd)/$@
	ln -s $(shell pwd)/$< $(shell pwd)/$@

$(LINKS_DIR)/%.png: $(EXTERNAL_DIR)/%.png
	rm -f $(shell pwd)/$@
	ln -s $(shell pwd)/$< $(shell pwd)/$@

# Finally we have the rules for making the actual plots
# ===================================================== #
$(GENERATED_DIR)/atmosphere_profile.png: plot_strobel_atm_profile.py
	python $< --save $@

$(GENERATED_DIR)/xz_context.png: plot_xz_context.py
	python $< --save $@

$(GENERATED_DIR)/shellfeyerabend6.png: plot_feyerabend6.py
	python $< --shell --save $@

$(GENERATED_DIR)/noshellfeyerabend6.png: plot_feyerabend6.py
	python $< --no-shell --save $@

$(GENERATED_DIR)/drape.png: plot_field_drape.sh
	./$< $(GENERATED_DIR)

$(GENERATED_DIR)/synthetic_spectrograms.png: plot_synthetic_spectrograms.py
	python $< --save $@

$(GENERATED_DIR)/wake_structure.png: plot_wake_structure.py
	python $< --save $@

$(GENERATED_DIR)/beta_pressure_shell.png: plot_beta_pressure.py
	python $< --shell --save $@

$(GENERATED_DIR)/beta_pressure_noshell.png: plot_beta_pressure.py
	python $< --no-shell --save $@

clean:
	rm -rf $(LINKS_DIR)
	rm -rf $(GENERATED_DIR)
