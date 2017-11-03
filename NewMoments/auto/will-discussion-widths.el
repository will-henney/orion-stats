(TeX-add-style-hook
 "will-discussion-widths"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("mn2e" "useAMS" "usenatbib")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("newtxmath" "varg")))
   (TeX-run-style-hooks
    "latex2e"
    "mn2e"
    "mn2e10"
    "newtxtext"
    "newtxmath"
    "graphicx"
    "siunitx"
    "astrojournals"
    "fixltx2e")
   (TeX-add-symbols
    '("ion" 2)
    '("ION" 2)
    '("fakesc" 1)
    "hii"
    "oiii"
    "nii"
    "sii"
    "siii"
    "ha"
    "kms"
    "los"
    "pos"
    "obs"
    "ins"
    "rms"
    "FS"
    "therm"
    "Efrac"
    "lnSfrac"
    "Sfrac"
    "champ"
    "turb"
    "oi")
   (LaTeX-add-labels
    "sec:plane-sky-versus"
    "fig:observed-vmean-sigma"
    "fig:gauss"
    "fig:observed-vmean-sigma-fwhm"
    "fig:obs-sigma-sigma"
    "sec:turb-contr-spectr"
    "fig:surf-bright-pdf"
    "fig:simulation-vmean-sigma"
    "fig:simulation-stats-evo")
   (LaTeX-add-bibliographies
    "BibdeskLibrary-slavoj")
   (LaTeX-add-counters
    "ion"))
 :latex)

