# GEDL
Relevant codes of the paper "GEDL: A General Encryption Method Based on Deep Learning"

GEDL applies a two-stage structure.

At the first stage, both parties in the communication get copies of the public training set and modify them under the instruction of the key, completing the construction of confidential synthetic training sets, respectively. And the synthetic training sets mastered by both parties are expected to be consistent. Afterward, the hyperparameters in the key instruct the training on the synthetic training sets. Hence a large number of parameters are generated, which can be arranged as weight vector tables, followed by a further process on them with the SHA-256 function to obtain codebooks. So far, the first stage called communication preparation ends.

At the second stage, when information requires transmitting, encryption and decryption are based on the codebooks. For a clear illustration, we consider two situations where text and images need transmitting, respectively. 
- For text transmission, assuming GEDL applies word embedding model, codebooks contain word keys and corresponding hashes. The sender refers to the codebook at hand and uses the plaintext as an index unit to obtain the corresponding ciphertext. And then the ciphertext is sent to the receiver. In turn, the receiver decrypts the ciphertext based on the mapping in the codebook, which is equivalently an inverted indexing operation. 
- For image transmission, assuming GEDL applies the Convolutional Neural Network (CNN) model, codebooks only contain hashes. The sender gets them in order from the codebook at hand and uses exclusive or (XOR) to mix them and pixels of the image to obtain an encrypted image. In turn, the receiver also gets hashes from the codebook in order and uses XOR to recover the original image.

After completing the transmission of information, both ends adjust the codebook in a certain way. Therefore, when the next information needs to be transmitted, it is encrypted based on the new codebook.

![image](https://github.com/tempAmbi/GEDL/tree/master/images/overview_conf.eps)

And the process of using the codebook is shown as the following figure.
For text encryption:
![image](https://github.com/tempAmbi/GEDL/tree/master/images/process2.eps)
For image encryption:
![image](https://github.com/tempAmbi/GEDL/tree/master/images/process_image.eps)

>A：Construction of Synthetic Corpus
>>
    Step 1: Get Wikipedia corpus resources
    Step 2: Process the wiki's xml file into a normal txt file--process_xml.py
    Step 3: Convert traditional txt to simplified txt using opencc(Chinese)
    Step 4: Participle--segmentation_Chinese.py or segmentation_English.py
    Step 5: Process incremental corpus--incremental_corpus_preprocess.py
    Step 6: Add incremental corpus to original corpus
>B: Training
>>
    Run word2vec_model.py for word2vec model
    Run fasttext.py for fasttext model
    As for other models, please refer to the corresponding source codes in github.
>C: Process the word vector table
>>
    Run table_process.py
>D: Some experiments
>>
    recovery.py
    frequency_analysis.py
    correlation_analysis_1.py
    correlation_analysis_2.py
    plaintext_sensitivity_analysis.py
    ciphertext_sensitivity_analysis.py
    efficiency_analysis.py
