# WordNet Format Conversion

### Article

Script to convert WordNet from XML/LMF format to Princeton WNDB used in the following article.

Branco, Ruben, João Rodrigues, Chakaveh Saedi and António Branco, 2019, "Assessing Wordnets with WordNet Embeddings", In Proceedings, 10th Global WordNet Conference (GWC2019), Poland, 23-27 July 2019.

## Using and adapting

The entrypoint for the script is the `main.py` file. Inside this file, a few essential arguments are set, such as the save path, the synset prefixes and the process to undertake (lmf to princeton or princeton to lmf).

There are a few xml handlers available by default, however, you may have to adapt in order to make the conversion as there are slight inconsistencies in semantic relation naming across the multiple wordnets that use the LMF format.

These handlers and their descriptions are available in the file `modules/all_xml_handlers.py`.

The conversion will generate logs and error files, in case anything goes wrong during the conversion.

## Requirements

Standard library of python3.
