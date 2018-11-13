GENERATED_DIR := generated_plots
EXTERNAL_DIR  := external_plots
ALL_DIR     := plots

GENERATED_PLOT_NAMES := atmosphere_profile.png xz_context.png shellfeyerabend6.png noshellfeyerabend6.png drape.png synthetic_spectrograms.png \
	wake_structure.png beta_pressure_shell.png beta_pressure_noshell.png single_spectrum.png rehearsal_comparison.png
GENERATED_PLOT_PATHS := $(addprefix $(GENERATED_DIR)/,$(GENERATED_PLOT_NAMES))
EXTERNAL_PLOT_NAMES  := mccomasfig7.png heather_scem_espec_no_footer.png mccomasfig6.png
EXTERNAL_PLOT_PATHS  := $(addprefix $(EXTERNAL_DIR)/,$(EXTERNAL_PLOT_NAMES))

ALL_PLOT_NAMES       := $(GENERATED_PLOT_NAMES) $(EXTERNAL_PLOT_NAMES)
ALL_PLOT_PATHS       := $(GENERATED_PLOT_PATHS) $(EXTERNAL_PLOT_PATHS)

ALL_ALL_PATHS      := $(addprefix $(ALL_DIR)/,$(ALL_PLOT_NAMES))

.PHONY: all install clean

all: $(ALL_ALL_PATHS)

# All the plots will eventually go into the all directory
# This makes sure that directory exists
$(ALL_PLOT_PATHS): | $(ALL_DIR)

$(ALL_DIR):
	mkdir -p $(ALL_DIR)

# In addition, the generated plots will also go in the generated plots directory
# This makes sure that directory exists
$(GENERATED_PLOT_PATHS): | $(GENERATED_DIR)

$(GENERATED_DIR):
	mkdir -p $(GENERATED_DIR)

# Copy every image in generated and external dirs to the all directory
$(ALL_DIR)/%.png: $(GENERATED_DIR)/%.png
	cp $(shell pwd)/$< $(shell pwd)/$@

$(ALL_DIR)/%.png: $(EXTERNAL_DIR)/%.png
	cp $(shell pwd)/$< $(shell pwd)/$@

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

$(GENERATED_DIR)/single_spectrum.png: sw_distribution.py
	python $< --save $@

$(GENERATED_DIR)/rehearsal_comparison.png: plot_rehearsal_comparison.py rehearsal_tools.py
	python $< --save $@

clean:
	rm -rf $(ALL_DIR)
	rm -rf $(GENERATED_DIR)

install:
	cp -r plots ~/Dropbox/Pluto-2017/
