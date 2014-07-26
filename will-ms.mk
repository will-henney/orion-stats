
MS=will-ms-changes

open-pdf: $(MS).pdf
	open $(MS).pdf

$(MS).pdf: $(MS).tex
	pdflatex $< ; pdflatex $< ; open $@
