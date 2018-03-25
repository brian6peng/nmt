import jieba
import os
import plac
import random


def cut(source_path, dest_path):
    if not os.path.exists(source_path):
        print('source path file does not exist, please check your file path')
        return

    with open(source_path, mode='r', encoding='utf-8') as fs:
        text = fs.read()

    seg_text = jieba.cut(text)
    outline = " ".join(seg_text)

    with open(dest_path, mode='w', encoding='utf-8') as fs:
        fs.write(outline)


def build_vocab_file(embedding_path, vocab_path, max_size=20000):
    if not os.path.exists(embedding_path):
        print(
            'word embedding file does not exist, please check your file path')
        return

    special_tokens = ["<unk>", "<s>", "</s>"]
    vocab_size = 0
    with open(vocab_path, 'w', encoding='utf-8') as dest:
        for special in special_tokens:
            dest.write(special + '\n')

        f = open(embedding_path, 'r', encoding='utf-8')
        f.readline() #skip first line
        for line in f:
            if vocab_size > max_size:
                break
            values = line.split()
            word = values[0]
            if word not in special_tokens:
                dest.write(word + '\n')
                vocab_size += 1
    f.close()


def build_sub_set(base_path, size):
    with open(
            os.path.join(base_path, 'train.zh'), 'r',
            encoding='utf-8') as file:
        zh_lines = file.readlines()
    with open(
            os.path.join(base_path, 'train.en'), 'r',
            encoding='utf-8') as file:
        en_lines = file.readlines()

    test_range = random.sample(range(len(zh_lines)), size)
    test_path = os.path.join(base_path, 'test.zh')
    with open(test_path, 'w', encoding='utf-8') as file:
        for index in test_range:
            file.write(zh_lines[index])
    test_path = os.path.join(base_path, 'test.en')
    with open(test_path, 'w', encoding='utf-8') as file:
        for index in test_range:
            file.write(en_lines[index])

    validate_range = random.sample(range(len(zh_lines)), size)
    validate_path = os.path.join(base_path, 'validate.zh')
    with open(validate_path, 'w', encoding='utf-8') as file:
        for index in validate_range:
            file.write(zh_lines[index])
    validate_path = os.path.join(base_path, 'validate.en')
    with open(validate_path, 'w', encoding='utf-8') as file:
        for index in validate_range:
            file.write(en_lines[index])


@plac.annotations(
    action=("data process action", "option", "c", str),
    base_dir=("base directory", "option", "p", str))
def main(action='cut', base_dir='/tmp/data/challenger/translation'):
    if action == 'cut':
        source_path = os.path.join(base_dir, 'train.zh')
        dest_path = os.path.join(base_dir, 'train_cut.zh')
        cut(source_path, dest_path)
        print('word cuting finish')
    elif action == 'vocab':
        embedding_path = os.path.join(base_dir, 'embedding/zh.vec')
        vocab_path = os.path.join(base_dir, 'vocab.zh')
        build_vocab_file(embedding_path, vocab_path)
        print('build zh vocab file finish')
        embedding_path = os.path.join(base_dir, 'embedding/en.vec')
        vocab_path = os.path.join(base_dir, 'vocab.en')
        build_vocab_file(embedding_path, vocab_path)
        print('build zh vocab file finish')
    elif action == 'sub':
        build_sub_set(base_dir, 5000)


if __name__ == '__main__':
    plac.call(main)