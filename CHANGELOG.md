28 March 2021

- Fixed an issue where all implicon but the very first one were shifted by 1. This applies to human and mouse, as well as the allele and non-allele-specific scripts. Thanks to Rexxi Prasaya for brining this to my attention.

- Explicitly defined the `col_character` classes for the visualisation scripts as `character` or `double`, as some columns were incorrectly auto-detected as `character` (and consequently prevented the plotting)
