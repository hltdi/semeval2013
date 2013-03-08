l1classifiers: l1de l1es l1fr l1it l1nl

l2classifiers: l2de l2es l2fr l2it l2nl

l1de:
	python3 pickle_l1_classifiers.py de
l1es:
	python3 pickle_l1_classifiers.py es
l1fr:
	python3 pickle_l1_classifiers.py fr
l1it:
	python3 pickle_l1_classifiers.py it
l1nl:
	python3 pickle_l1_classifiers.py nl

l2de:
	python3 train_extracted_level2.py de
l2es:
	python3 train_extracted_level2.py es
l2fr:
	python3 train_extracted_level2.py fr
l2it:
	python3 train_extracted_level2.py it
l2nl:
	python3 train_extracted_level2.py nl

l1experiments: l1_exp_de l1_exp_es l1_exp_fr l1_exp_it l1_exp_nl

l1_exp_de:
	./run_one_l1_language.sh de
l1_exp_es:
	./run_one_l1_language.sh es
l1_exp_fr:
	./run_one_l1_language.sh fr
l1_exp_it:
	./run_one_l1_language.sh it
l1_exp_nl:
	./run_one_l1_language.sh nl

l2experiments: l2_exp_de l2_exp_es l2_exp_fr l2_exp_it l2_exp_nl
l2_exp_de:
	python3 run_experiment_l2.py de
l2_exp_es:
	python3 run_experiment_l2.py es
l2_exp_fr:
	python3 run_experiment_l2.py fr
l2_exp_it:
	python3 run_experiment_l2.py it
l2_exp_nl:
	python3 run_experiment_l2.py nl

mrf_experiments: mrf_coach mrf_education mrf_execution mrf_figure mrf_job mrf_letter mrf_match mrf_mission mrf_mood mrf_paper mrf_post mrf_pot mrf_range mrf_rest mrf_ring mrf_scene mrf_side mrf_soil mrf_strain mrf_test

mrf_coach:
	python3 run_experiment_mrf.py --sourceword=coach --trialdir=../finaltest
mrf_education:
	python3 run_experiment_mrf.py --sourceword=education --trialdir=../finaltest
mrf_execution:
	python3 run_experiment_mrf.py --sourceword=execution --trialdir=../finaltest
mrf_figure:
	python3 run_experiment_mrf.py --sourceword=figure --trialdir=../finaltest
mrf_job:
	python3 run_experiment_mrf.py --sourceword=job --trialdir=../finaltest
mrf_letter:
	python3 run_experiment_mrf.py --sourceword=letter --trialdir=../finaltest
mrf_match:
	python3 run_experiment_mrf.py --sourceword=match --trialdir=../finaltest
mrf_mission:
	python3 run_experiment_mrf.py --sourceword=mission --trialdir=../finaltest
mrf_mood:
	python3 run_experiment_mrf.py --sourceword=mood --trialdir=../finaltest
mrf_paper:
	python3 run_experiment_mrf.py --sourceword=paper --trialdir=../finaltest
mrf_post:
	python3 run_experiment_mrf.py --sourceword=post --trialdir=../finaltest
mrf_pot:
	python3 run_experiment_mrf.py --sourceword=pot --trialdir=../finaltest
mrf_range:
	python3 run_experiment_mrf.py --sourceword=range --trialdir=../finaltest
mrf_rest:
	python3 run_experiment_mrf.py --sourceword=rest --trialdir=../finaltest
mrf_ring:
	python3 run_experiment_mrf.py --sourceword=ring --trialdir=../finaltest
mrf_scene:
	python3 run_experiment_mrf.py --sourceword=scene --trialdir=../finaltest
mrf_side:
	python3 run_experiment_mrf.py --sourceword=side --trialdir=../finaltest
mrf_soil:
	python3 run_experiment_mrf.py --sourceword=soil --trialdir=../finaltest
mrf_strain:
	python3 run_experiment_mrf.py --sourceword=strain --trialdir=../finaltest
mrf_test:
	python3 run_experiment_mrf.py --sourceword=test --trialdir=../finaltest

## target to extract all the training data in parallel
extract_all_training: extract_de extract_es extract_fr extract_it extract_nl
extract_de:
	./extract_onelanguage_training.sh de
extract_es:
	./extract_onelanguage_training.sh es
extract_fr:
	./extract_onelanguage_training.sh fr
extract_it:
	./extract_onelanguage_training.sh it
extract_nl:
	./extract_onelanguage_training.sh nl
