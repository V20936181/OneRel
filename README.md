### This a modified forked repo of China-ChallengeHub/OneRel
## OneRel: Joint Entity and Relation Extraction with One Model in One Step

This repository contians the source code and datasets for the paper: **OneRel: Joint Entity and Relation Extraction with One Model in One Step**, Yu-Ming Shang, Heyan Huang and Xian-Ling Mao, AAAI-2022.

## Usage

1. **Environment**
   ```shell
   cd OneRel
   conda env create -f onerel_env_droplet.yml
   conda activate onerel
   ```

2. **The pre-trained BERT**

    The pre-trained BERT (bert-base-cased) will be downloaded automatically after running the code. Alternatively, you can manually download the pre-trained BERT model and save it to `./pre_trained_bert` using cmd below.
   ```shell
   pip install -U "huggingface_hub[cli]"
   huggingface-cli download NeuML/pubmedbert-base-embeddings --local-dir {ABSOLUTE_PATH_TO_PRE_TRAINED_BERT_FOLDER}
   ```


4. **Train the model (take NYT as an example)**

    Modify the second dim of `batch_triple_matrix` in `data_loader.py` to the number of relations, and run

    ```shell
    python train.py --dataset=NYT --batch_size=8 --rel_num=24 
    ```
    The model weights with best performance on dev dataset will be stored in `checkpoint/NYT/`

5. **Evaluate on the test set (take NYT as an example)**

    Modify the `model_name` (line 48) to the name of the saved model, and run 
    ```shell
    python train.py --dataset=BioRED --batch_size=8 --rel_num=8
    ```

    The extracted results will be save in `result/BioRED`.


