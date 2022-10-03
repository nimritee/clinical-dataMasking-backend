from __future__ import print_function
from neuroner import neuromodel
import warnings
warnings.filterwarnings('ignore')

neuromodel.fetch_data('conll2003')
neuromodel.fetch_data('example_unannotated_texts')
neuromodel.fetch_data('i2b2_2014_deid')

neuromodel.fetch_model('i2b2_2014_glove_spacy_bioes')
nn = neuromodel.NeuroNER(train_model=False, use_pretrained_model=True, dataset_text_folder="data/example_unannotated_texts",
pretrained_model_folder="trained_models/i2b2_2014_glove_spacy_bioes", output_folder="output/", spacylanguage="en_core_web_sm") 

nn.fit()
nn.close()
# dataset_text_folder=./data/example_unannotated_texts --pretrained_model_folder=./trained_models/i2b2_2014_glove_spacy_bioes --output_folder=./output/ --spacylanguage=en_core_web_sm