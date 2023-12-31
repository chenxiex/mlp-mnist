import warnings
import argparse
from sklearn.datasets import fetch_openml
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import log_loss
from joblib import dump,load
import time

# 定义训练函数
def train(model,X_train,y_train):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=ConvergenceWarning,module="sklearn")
        model.fit(X_train,y_train)

# 定义测试函数
def test(model,X_test,y_test):
    test_loss=log_loss(y_test,model.predict_proba(X_test))
    correct=0
    y_pred=model.predict(X_test)
    for i in range(len(y_test)):
        if y_pred[i]==y_test[i]:
            correct+=1
    length=len(y_test)
    print('测试结果：平均损失函数值：{:.4f},正确率：{}/{} ({:.0f}%)'.format(test_loss,correct,length,100.*correct/length))

def main():
    # 测试参数
    parser=argparse.ArgumentParser(description="MNIST MLP分类器")
    parser.add_argument('--batch-size',type=int,default=64,metavar='N',help='输入批次大小，默认为64')
    parser.add_argument('--epochs',type=int,default=14,metavar='N',help='训练轮数，默认为14')
    parser.add_argument('--lr',type=float,default=0.01,metavar='LR',help='学习率，默认为0.01')
    parser.add_argument('--gamma',type=float,default=0,metavar='M',help='学习率衰减率，默认为0')
    parser.add_argument('--seed',type=int,default=1,metavar='S',help='随机种子，默认为1')
    parser.add_argument('--save-model',action='store_true',default=False,help='是否保存模型，默认为False')
    args=parser.parse_args()

    #数据集
    X,y=fetch_openml("mnist_784",version=1,return_X_y=True,as_frame=False,parser="pandas")
    # transform
    X=(X/255.0)
    # 划分测试与训练集
    X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=0,test_size=10000)

    #模型定义
    model=MLPClassifier(hidden_layer_sizes=(1000,100,40,20,),
                        max_iter=1,
                        solver='sgd',
                        batch_size=args.batch_size,
                        learning_rate='invscaling',
                        learning_rate_init=args.lr,
                        power_t=args.gamma,
                        random_state=args.seed,
                        warm_start=True)

    #训练
    start=time.time()
    for epoch in range(1,args.epochs+1):
        train(model,X_train,y_train)
        test(model,X_test,y_test)
    end=time.time()
    print('训练时间：{:.2f}s'.format(end-start))

    #保存模型
    if args.save_model:
        dump(model,'mlp-mnist.joblib')


if __name__ == '__main__':
    main()