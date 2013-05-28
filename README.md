semeval2013
===========

Our entry for the SemEval 2013 CL-WSD task.

For a description of the task, please see:
http://www.cs.york.ac.uk/semeval-2013/task10/

For a detailed description of our approach, please see the paper in paper/ !

collaborators
=============
  * Alex Rudnick
  * Can Liu
  * Michael Gasser

details
=======
Runs under Python 3 with NLTK.

GPL v3 for our code.
Berkeley code is free for research and education use.
NLTK is Apache 2.0, but is not included in this repository.

We also depend on TreeTagger, which is available here:
http://www.ims.uni-stuttgart.de/forschung/ressourcen/werkzeuge/treetagger.html

TreeTagger is not redistributable (sorry!), so you should unzip the appropriate
files into the TreeTagger directory. We want to get rid of this dependency so
the whole setup is redistributable. Ask Helmut to release the source. (we've
made modifications to the tiny tagging Perl scripts for use with this project)

Continuing development on the system, and integration into our RBMT system, will
show up at http://github.com/alexrudnick/clwsd !
