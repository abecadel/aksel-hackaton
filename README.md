### aksel-mercari-hackaton

# ML and AR solution for enhancing seller experience on platforms like Mercari

Seller uses mobile phone camera to automatically identify an item and is presented with the sale potential of that item i.e. estimated price, current market demand, time to close the transaction.
Item identification is achieved using Deep Learning techniques.
Sale potential is estimated from historical data (search results, closed/unclosed transactions etc.).
The results are presented to the user on a smartphone screen.
Our prototype will use open source ML frameworks for object recognition and predictions.
Historical sales data will be based on a public Kaggle datasets.


### Technical stack
1. Python 3.6
1. Flask
1. Pandas
1. OpenCv
1. Tensorflow
1. Html5+CSS3
1. Client would be any smartphone with webbrowser

### We'll use data from:
1. https://www.kaggle.com/c/mercari-price-suggestion-challenge (with data augmentation) for estimating sale potential
1. pretrained model from https://github.com/tensorflow/models/tree/master/research/object_detection (training this kind of model from scratch on datasets like Coco takes way to long and it wouldn't finish in 24h) for object detection and apply transfer learning for new classes.
