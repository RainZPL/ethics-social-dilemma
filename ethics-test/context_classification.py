import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

# 加载情感分析器
sia = SentimentIntensityAnalyzer()

# 加载停用词
stop_words = set(stopwords.words('english'))

# 加载伦理类别标签
LABELS = ['normal', 'hateful', 'offensive']

# 定义模型
def classify_text(text):
    # 分词并过滤停用词
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    
    # 进行情感分析
    sentiment_score = sia.polarity_scores(text)
    
    # 组合情感得分和文本特征，作为分类器的输入
    features = {
        'neg': sentiment_score['neg'],
        'neu': sentiment_score['neu'],
        'pos': sentiment_score['pos'],
        'compound': sentiment_score['compound'],
        'contains_hate': any(word in filtered_words for word in ['hate', 'violence', 'threat']),
        'contains_offensive': any(word in filtered_words for word in ['offensive', 'inappropriate', 'disturbing']),
    }
    
    # 使用训练好的分类器对文本进行分类
    return classifier.classify(features)

# 加载训练数据，格式为（文本，标签）
train_data = [
    ("This is a normal sentence.", "normal"),
    ("I hate you and hope you die.", "hateful"),
    ("Your skin color is disgusting.", "offensive"),
    ("This is an offensive comment.", "offensive"),
    ("I disagree with your opinion, but respect your right to express it.", "normal"),
    ("I will punch you in the face if you don't do what I say.", "hateful"),
    ("This is a peaceful protest for justice.", "normal"),
    ("I am going to kill you.", "hateful"),
]

# 提取特征，格式为（特征，标签）
train_features = []
for text, label in train_data:
    features = classify_text(text)
    train_features.append((features, label))

# 训练分类器
classifier = nltk.NaiveBayesClassifier.train(train_features)

# 使用分类器进行分类
text = "I will kill you if you don't do what I say."
category = classify_text(text)

# 输出分类结果
print(f"The text '{text}' is classified as '{category}'")
