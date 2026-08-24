SCAD    ?= organizer_box.scad
STL     ?= organizer_box_100x200x64_rib1.33.stl
REF     ?= $(HOME)/Downloads/200x100_4_V2.stl
BUILD   ?= build

OPENSCAD ?= openscad
CAMERA   := 0,0,0,62,0,32,0

.PHONY: all clean validate verify preview embed

all: $(STL) embed

# The web app hands out the model as OpenSCAD source, so keep its copy in step.
embed: $(SCAD)
	python3 tools/embed_scad.py

$(STL): $(SCAD)
	$(OPENSCAD) -o $@ --export-format binstl $(SCAD)

# Re-create the source box (rib = 2 mm) so it can be diffed against the original.
$(BUILD)/validation_rib2.stl: $(SCAD)
	@mkdir -p $(BUILD)
	$(OPENSCAD) -o $@ --export-format binstl -D rib=2 $(SCAD)

validate: $(BUILD)/validation_rib2.stl
	cd tools && python3 compare_stl.py $(REF) ../$(BUILD)/validation_rib2.stl \
		--dz 34 --step 2.3 --tol 0.06

verify: $(STL)
	cd tools && python3 verify_final.py ../$(STL)

preview: $(STL)
	@mkdir -p $(BUILD)
	@printf 'import("../%s");\n' "$(STL)" > $(BUILD)/_preview.scad
	$(OPENSCAD) -o $(BUILD)/preview_new.png --imgsize=1100,850 --colorscheme=Tomorrow \
		--autocenter --viewall --camera=$(CAMERA) $(BUILD)/_preview.scad
	@rm -f $(BUILD)/_preview.scad

clean:
	rm -rf $(BUILD) tools/__pycache__
