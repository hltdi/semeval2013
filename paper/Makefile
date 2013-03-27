NAME=semeval2013

$(NAME).pdf: $(NAME).tex $(NAME).bib pentagram.pdf
	pdflatex $(NAME)
	bibtex $(NAME)
	pdflatex $(NAME)
	pdflatex $(NAME)

pentagram.pdf: pentagram.dot
	neato -Tpdf pentagram.dot -o pentagram.pdf

clean:
	rm -f pentagram.pdf *.bbl *.blg *.out *.aux *.log *.Rout .RData $(NAME).pdf
