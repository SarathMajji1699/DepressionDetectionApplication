![Total Lines of Code](https://img.shields.io/badge/total%20lines%20of%20code-1516-green?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/SarathMajji1699/DepressionDetectionApplication?style=for-the-badge)
![GitHub followers](https://img.shields.io/github/followers/SarathMajji1699?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues-raw/SarathMajji1699/DepressionDetectionApplication?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/SarathMajji1699/DepressionDetectionApplication?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/SarathMajji1699/DepressionDetectionApplication?style=for-the-badge)
![Maintenance](https://img.shields.io/maintenance/yes/2021?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/SarathMajji1699/DepressionDetectionApplication?style=for-the-badge)

# DEPRESSION DETECTION APPLICATION
<p align="center">
  <a href="https://github.com/SarathMajji1699/DepressionDetectionApplication">
    <img src="https://github.com/SarathMajji1699/ImagesUpload/blob/main/logo.jpg?raw=true" alt="Logo">
  </a>

  <h2 align="center">Depression Detection Application</h2>

  <p align="center">
   <h1> <strong>About the Project</strong></h1>
The main idea of this project is to analyze the text whether it is 'NORMAL' or 'DEPRESSIVE' using CNN model. We have included 4 options in our project ,they are:
<br/>
<ul>
<li>Text Field</li>
<li>File Upload (for bulk data)</li>
<li>Image Upload (image with text)</li>
<li>Twitter username for extracting his/her last 10 tweets for analyzing</li>
</ul>

### Heroku
We have deployed it in
[heroku](http://sarathmajji-dda.herokuapp.com/)
cloud platform.

### Dataset
We have taken the dataset from
[kaggle](https://www.kaggle.com/kazanova/sentiment140)
which is training.1600000.processed.noemoticon.csv.<br>
We have also used
[GoogleNews-vectors-negative300](https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz)
for embedding technique.

### Built With
<ul>
<li>Pandas</li>
<li>Numpy</li>
<li>Tensorflow</li>
<li>Keras</li>
<li>Flask</li>
<li>CNN</li>
<li>Opencv-python</li>
<li>Smptlib</li>
<li>PostgreSQL Database</li>
<li>Tweepy</li>
<li>Pillow</li>
<li>Pytesseract</li>
<li>SQLAlchemy</li>
<li>Heroku Cloud Platform</li>
<li>Android Studio</li>
</ul>
    <br />
   <h1> <strong>Description of Project</h1></strong>
   <ul>
   <li>In Depression Detection Application project we have used convolutional neural networks to analyze the text and display the result i.e, 'NORMAL' or 'DEPRESSIVE'.</li>
   <li>The objective is to use the data from social media networks to explore various methods of early detection of MDDs based on machine learning and deep learning techniques. We performed a thorough analysis of the dataset to characterize the subjects behavior based on different aspects of their writings i.e, textual spreading.</li>
   <li>We have included login and registeration process in our project so that the user can subscribe the twitter users for monitoring his tweet whether it is 'NORMAL' or 'DEPRESSIVE'.</li>
   <li>We have also created an android app for our project using android studio.</li>
</p>
<!-- GETTING STARTED -->
<p>

## Getting Started

To get a local copy up and running follow these simple steps.

## Prerequisites

This is an example of how to list the packages that you need to run this project.

  ```sh
  cd DepressionDetectionApplication
  cat requirements.txt
  ```

## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/SarathMajji1699/DepressionDetectionApplication.git
   ```
2. Install required packages
   ```sh
   $ pip install -r requirements.txt
   ```



<!-- USAGE EXAMPLES -->
## Usage
1. Train the Model
   ```sh
   $ cd DepressionDetectionApplication
   $ python3 CNN-final-model.ipynb
   ```
2. Run the Model
   ```sh
   $ python3 app.py
   ```
</p>
