# Image Crop Reproducibility

All image-cropping operations (spread-to-page splits, word-level crops, etc.) must record enough data to **reproduce the crop programmatically at any image resolution**.

1. **Dual storage.** Crop coordinates are stored both (a) as metadata embedded in the output image file (PNG tEXt chunks or JPEG EXIF) and (b) in an independent JSON file (`../book-of-job/out/cam1753-crops.json` for word crops). Either copy is authoritative on its own.

2. **Absolute coordinates with source dimensions.** Always record pixel-level absolute coordinates together with the source image dimensions they were measured against (e.g. `bbox_abs` + `page_size`). This makes the data resolution-independent without requiring separate relative coordinates: `frac = abs_coord / source_dim`, then `new_coord = frac * new_source_dim`.

3. **Relative coordinates are redundant but welcome.** When a crop editor produces relative coordinates (e.g. `bbox_rel`), store them alongside the absolute ones. The redundancy serves as a cross-check and may be convenient for editor state restoration, but the absolute coordinates plus source dimensions are the primary record.

4. **Overwrite-on-re-crop.** The persistent JSON uses SID as key. Re-cropping an image overwrites the previous entry; git history preserves the full edit trail if needed.
