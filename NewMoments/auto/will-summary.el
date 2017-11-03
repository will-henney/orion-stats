(TeX-add-style-hook
 "will-summary"
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
    "booktabs"
    "siunitx"
    "astrojournals"
    "fixltx2e")
   (TeX-add-symbols
    '("ion" 2)
    '("ION" 2)
    '("fakesc" 1)
    "hii"
    "oi"
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
    "denfrac"
    "lnSfrac"
    "Sfrac")
   (LaTeX-add-labels
    "sec:summary-conclusions"
    "fig:causality-flow")
   (LaTeX-add-bibliographies
    "BibdeskLibrary-slavoj")
   (LaTeX-add-counters
    "ion"))
 :latex)

