from __future__ import print_function
from neuroner import neuromodel
import warnings
warnings.filterwarnings('ignore')

# neuromodel.fetch_data('conll2003')
# neuromodel.fetch_data('unannotated_texts')
# neuromodel.fetch_data('i2b2_2014_deid')
def call_nerm():
    neuromodel.fetch_model('i2b2_2014_glove_spacy_bioes')
    nn = neuromodel.NeuroNER(train_model=False, use_pretrained_model=True, dataset_text_folder="data/input/unannotated_texts",
    pretrained_model_folder="nerm/trained_models/i2b2_2014_glove_spacy_bioes", output_folder="data/mask_input", spacylanguage="en_core_web_sm") 
    nn.fit()
    nn.close()

call_nerm()