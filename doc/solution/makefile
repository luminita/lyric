all: solution.pdf

REFS = solution.bib

solution.pdf: solution.tex 

%.pdf: %.tex
	pdflatex $*.tex
	if ( grep -q citation $*.aux ) ; then \
		bibtex $* ; \
		pdflatex $*.tex ; \
	fi;
	pdflatex $*.tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.toc
