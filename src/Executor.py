
import Vgg16
import Vgg16BN
from IPython.display import FileLink

class Executor:

    def __init(self):
        self.vgg = None
        self.batch_size = None
        self.train_batches = None
        self.val_batches = None
        self.data_path = None

    def and_(self):
        return self;

    def set_Vgg(self, vgg):
        self.vgg = vgg

    def init_validation_and_training_data(self):
        train_path = self.data_path+"train"
        val_path = self.data_path+"valid"

        self.train_batches = self.vgg.get_batches(batch_size=self.batch_size, path=train_path)
        self.val_batches = self.vgg.get_batches(batch_size=self.batch_size, path=val_path)

        print("initialized training data from: "+train_path)
        print("initialized validation data from: "+val_path)

    def finetune_only_softmax_layer_for_epochs(self, num_epochs):
        self.vgg.finetune(self.train_batches)
        self.vgg.fit(self.train_batches, self.val_batches, nb_epoch=num_epochs)
        print("Vgg model finetuned.")
        return self;

    def save_model_to_file(self, fileName):
        self.vgg.model.save_weights(fileName)
        return self;

    def load_model_from_file(self, fileName):
        self.vgg.model.load_weights(fileName)
        return self;

    def build_predictions_on_test_data(self):
        test_path = self.data_path + "test"
        b, p= self.vgg.test(test_path, batch_size=2)

        self.prediction = zip([name[8:] for name in b.filenames], p.astype('str'))
        return self;

    def save_predictions_to_file(self, fileName):
        outF = open(fileName, 'w')
        outF.write('image_name,Type_1,Type_2,Type_3\n')

        for elem in self.prediction:
            outF.write(elem[0] + ',' + ','.join(elem[1]) + '\n')
        outF.close()
        FileLink(fileName)
        return self;

class ExecutorBuilder:

    def __init__(self):
        self.executor = Executor()

    def and_(self):
        return self.executor

    def with_Vgg16(self):
        vgg16 = Vgg16()
        self.executor.set_Vgg(vgg16)
        return self.executor

    def with_Vgg16BN(self):
        vgg16 = Vgg16BN()
        self.executor.set_Vgg(vgg16)
        return self.executor

    def data_on_path(self, data_folder):
        self.executor.data_path = data_folder
        self.executor.init_validation_and_training_data()
        return self.executor

    def batch_size(self, batch_size):
        self.executor.batch_size = batch_size
        return self.executor

    def build(self):
        return self.executor
