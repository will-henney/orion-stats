
MS=will-ms-changes
WILLFIGS=sf-vs-3d-panels.pdf vca-thin-vs-3d-panels.pdf vca-thick-vs-3d-panels.pdf

all: tar-file-for-jane open-pdf


tar-file-for-jane: ms-resubmit-will.tar.gz

ms-resubmit-will.tar.gz: ms-resubmit-will.tex will-replies.org $(WILLFIGS)
	tar -zcf $@ $^

open-pdf: $(MS).pdf
	open $(MS).pdf

$(MS).pdf: $(MS).tex
	pdflatex $< ; pdflatex $< ; open $@
