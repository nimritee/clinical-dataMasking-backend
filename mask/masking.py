from os import listdir, path, mkdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import importlib
from brat_parser import get_entities_relations_attributes_groups


class Configuration():

    def __init__(self, configuration="mask/configuration.cnf"):
        self.conf = configuration
        conf_doc = ET.parse(self.conf)
        root = conf_doc.getroot()
        self.entities_list = []
        for elem in root:
            if elem.tag == "plugins":
                for entities in elem:
                    entity = {}
                    for ent in entities:
                        entity[ent.tag] = ent.text
                    self.entities_list.append(entity)
            if elem.tag == "dataset":
                for ent in elem:
                    if ent.tag == "dataset_location":
                        self.dataset_location = ent.text
                    if ent.tag == "data_output":
                        self.data_output = ent.text

def get_data_sequences(file):
  ann_data = get_entities_relations_attributes_groups("data/mask_input/unnotated_texts_nerm/brat/deploy/"+ file + ".ann")
  sequences = []
  for key,values in ann_data[0].items():
    data =(values.text,values.type, values.span[0][0],values.span[0][1])
    sequences.append(data)
  return sequences


def masking_process(type,result,new_text):
    for i in range(0, len(result)):
        if type["masking_type"] == "Mask":
            masking_class = type['masking_class']
            plugin_module = importlib.import_module("masking_plugins." + masking_class)
            class_masking = getattr(plugin_module, masking_class)
            masking_instance = class_masking()
            
        if result[i][1] == type["entity_name"]:
            if type["masking_type"] == "Redact":
                new_token = "XXX"
            elif type["masking_type"] == "Mask":
                new_token = masking_instance.mask(result[i][0])
            print ("----------------------- " + result[i][1] + " ----------------")
            old_token = result[i][0]
            print (old_token+ " ---> " + new_token)
            new_text = new_text.replace(old_token, new_token)
    return new_text


def apply_masking(file, text, plugins):
    new_text = text
    for type in plugins:
        result = get_data_sequences(file[:-4])
        new_text = masking_process(type,result,new_text)
    return new_text


def main():
    print("\n Welcome to NERM Group Masking \n")

    cf = Configuration()
    data = [f for f in listdir(cf.dataset_location) if isfile(
        join(cf.dataset_location, f))]
    plugins = []
    for entity in cf.entities_list:
      masking_type = entity['masking_type']
      entity_name = entity['entity_name']
      if masking_type == "Redact":
          masking_class = ""
      else:
          masking_class = entity['masking_class']

      plugins.append({"masking_type":masking_type, "entity_name":entity_name, "masking_class":masking_class})
    
    for file in data:
        text = open(cf.dataset_location+"/"+file, 'r').read()
        new_text = apply_masking(file,text,plugins)

        # Write the output
        if not path.exists(cf.data_output):
            mkdir(cf.data_output)

        file_handler = open(cf.data_output + "/" + file, "w")
        file_handler.write(new_text)
        file_handler.close()


if __name__=="__main__":
    main()
