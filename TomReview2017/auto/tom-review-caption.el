(TeX-add-style-hook
 "tom-review-caption"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("mnras" "usenatbib")))
   (TeX-run-style-hooks
    "latex2e"
    "mnras"
    "mnras10"
    "graphicx")
   (LaTeX-add-bibliographies
    "arthur-henney"))
 :latex)

