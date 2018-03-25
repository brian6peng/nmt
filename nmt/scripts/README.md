# 中英文翻译数据预处理

1. 中文分词, **分词完成后需要把train.zh重命名，使用分词后的文件进行训练**

    `python data_process.py -c cut  -p /tmp/data/challenger/translation` 
2. 生成词向量

    `./fasttext skipgram -input /mnt/c/tmp/data/challenger/translation/train_cut.zh -output /mnt/c/tmp/data/challenger/translation/embedding/zh -minn 2 -maxn 5 -dim 300 -epoch 5 -thread 8`

    `./fasttext skipgram -input /mnt/c/tmp/data/challenger/translation/train.en -output /mnt/c/tmp/data/challenger/translation/embedding/en -minn 2 -maxn 5 -dim 300 -epoch 5 -thread 8`
3. 生成词典文件

    `python data_process.py -c vocab  -p /tmp/data/challenger/translation`
3. 生成测试集和验证集

    `python data_process.py -c sub  -p /tmp/data/challenger/translation`
4. 训练nmt

    `python -m nmt.nmt --attention=scaled_luong --src=zh --tgt=en --vocab_prefix=/tmp/data/challenger/translation/vocab --train_prefix=/tmp/data/challenger/translation/train --dev_prefix=/tmp/data/challenger/translation/validate --test_prefix=/tmp/data/challenger/translation/test --out_dir=/tmp/model/nmt --num_train_steps=12000 --steps_per_stats=100 --num_layers=2 --num_units=128 --dropout=0.2 --metrics=bleu`
5. 测试翻译

    `python -m nmt.nmt --out_dir=/tmp/model/nmt --inference_input_file=/tmp/data/challenger/translation/inference/infer.zh --inference_output_file=/tmp/data/challenger/translation/inference/infer_out.en`