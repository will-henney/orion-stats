(TeX-add-style-hook
 "will-discussion-scales"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("mnras" "useAMS" "usenatbib")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("newtxmath" "varg")))
   (TeX-run-style-hooks
    "latex2e"
    "mnras"
    "mnras10"
    "newtxtext"
    "newtxmath"
    "graphicx"
    "booktabs"
    "siunitx"
    "fixltx2e")
   (TeX-add-symbols
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
    "turb"
    "FS"
    "therm"
    "Efrac"
    "denfrac"
    "lnSfrac"
    "Sfrac")
   (LaTeX-add-labels
    "sec:what-significance-22"
    "sec:does-veloc-turb"
    "sec:toy-model-surface"
    "fig:fake-powerspec")
   (LaTeX-add-bibliographies
    "BibdeskLibrary-slavoj"))
 :latex)

